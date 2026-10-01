export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', '*');

  if (req.method === 'OPTIONS') {
    return res.status(204).end();
  }

  const host = req.headers.host || '';
  const proto = req.headers['x-forwarded-proto'] || 'https';
  const currentUrl = `${proto}://${host}`;

  return res.status(200).json({
    currentUrl,
    addresses: [
      {
        interface: 'Vercel Edge / Global CDN',
        ip: host,
        url: currentUrl
      }
    ],
    port: 443,
    provider: 'Vercel'
  });
}
