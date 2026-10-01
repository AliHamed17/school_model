import express from 'express';
import path from 'path';
import fs from 'fs';
import os from 'os';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;
const HOST = '0.0.0.0';

// Enable CORS for all requests so any device or web client can access resources
app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', '*');
  res.setHeader('Access-Control-Expose-Headers', 'Content-Length, Content-Disposition');
  if (req.method === 'OPTIONS') {
    return res.sendStatus(204);
  }
  next();
});

// Explicit download handler with Content-Disposition: attachment
// Ensures 100% reliable downloads on iOS Safari, Android Chrome, Chromebooks, and Windows
app.get('/downloads/:filename', (req, res) => {
  const filename = req.params.filename;
  const safeFilename = path.basename(filename);
  const filePath = path.join(__dirname, 'downloads', safeFilename);

  if (!fs.existsSync(filePath)) {
    return res.status(404).send('Download file not found');
  }

  res.setHeader('Content-Type', 'application/zip');
  res.setHeader('Content-Disposition', `attachment; filename="${safeFilename}"`);
  res.sendFile(filePath);
});

// Network information endpoint for student connection assistance
app.get('/api/network-info', (req, res) => {
  const interfaces = os.networkInterfaces();
  const addresses = [];

  for (const name of Object.keys(interfaces)) {
    for (const iface of interfaces[name] || []) {
      if (!iface.internal && iface.family === 'IPv4') {
        addresses.push({
          interface: name,
          ip: iface.address,
          url: `http://${iface.address}:${PORT}`
        });
      }
    }
  }

  const host = req.get('host');
  const protocol = req.protocol;
  const currentUrl = `${protocol}://${host}`;

  res.json({
    currentUrl,
    addresses,
    port: PORT
  });
});

// Serve static assets from project root
app.use(express.static(__dirname, {
  setHeaders: (res, filePath) => {
    // Add CORS to all static files
    res.setHeader('Access-Control-Allow-Origin', '*');
    if (filePath.endsWith('.zip')) {
      res.setHeader('Content-Disposition', `attachment; filename="${path.basename(filePath)}"`);
    }
  }
}));

// Route for root path
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Global error handler
app.use((err, req, res, next) => {
  console.error('[Server Error]', err);
  res.status(500).send('Internal Server Error');
});

app.listen(PORT, HOST, () => {
  console.log(`\n======================================================`);
  console.log(`AI CLASS SERVER RUNNING ON PORT ${PORT} (${HOST})`);
  console.log(`Local machine URL: http://localhost:${PORT}`);
  console.log(`Network URLs for student devices:`);
  
  const interfaces = os.networkInterfaces();
  for (const name of Object.keys(interfaces)) {
    for (const iface of interfaces[name] || []) {
      if (!iface.internal && iface.family === 'IPv4') {
        console.log(`  -> http://${iface.address}:${PORT} (${name})`);
      }
    }
  }
  console.log(`======================================================\n`);
});
