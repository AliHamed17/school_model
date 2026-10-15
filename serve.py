#!/usr/bin/env python3
"""Classroom file server.

Behaves like `python -m http.server` (read-only: GET and HEAD only, serves only this folder,
no uploads) with one addition: HTTP Range support. Browsers need Range requests to jump
around inside a video, so without it the tutorial video's chapter buttons and timeline
scrubbing do not work.

Usage:  python serve.py [PORT] [BIND_ADDRESS]      (defaults: 8000 0.0.0.0)
"""
import email.utils
import http.server
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    _remaining = None   # bytes left to send for the current ranged response

    def send_head(self):
        header = self.headers.get("Range")
        path = self.translate_path(self.path)
        if header and os.path.isfile(path):
            m = re.fullmatch(r"bytes=(\d*)-(\d*)", header.strip())
            if m and (m.group(1) or m.group(2)):
                size = os.path.getsize(path)
                if m.group(1):
                    start = int(m.group(1))
                    end = int(m.group(2)) if m.group(2) else size - 1
                else:                                   # "last N bytes"
                    start = max(0, size - int(m.group(2)))
                    end = size - 1
                end = min(end, size - 1)
                if start >= size or start > end:
                    self.send_response(416)
                    self.send_header("Content-Range", f"bytes */{size}")
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return None
                try:
                    f = open(path, "rb")
                except OSError:
                    self.send_error(404, "File not found")
                    return None
                f.seek(start)
                self._remaining = end - start + 1
                self.send_response(206)
                self.send_header("Content-Type", self.guess_type(path))
                self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
                self.send_header("Content-Length", str(self._remaining))
                self.send_header("Last-Modified", email.utils.formatdate(os.stat(path).st_mtime, usegmt=True))
                self.end_headers()
                return f
        return super().send_head()

    def copyfile(self, source, outputfile):
        try:
            if self._remaining is None:
                super().copyfile(source, outputfile)
                return
            left = self._remaining
            while left > 0:
                chunk = source.read(min(65536, left))
                if not chunk:
                    break
                outputfile.write(chunk)
                left -= len(chunk)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass        # the browser cancelled the download (normal when seeking in a video)

    def end_headers(self):
        self.send_header("Accept-Ranges", "bytes")
        super().end_headers()


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    bind = sys.argv[2] if len(sys.argv) > 2 else "0.0.0.0"
    os.chdir(ROOT)
    with http.server.ThreadingHTTPServer((bind, port), Handler) as httpd:
        print(f"Serving {ROOT} on {bind}:{port}  (Ctrl+C to stop)", flush=True)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()
