import express from 'express';
import cors from 'cors';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PORT = process.env.PORT || 3001;
const isProd = process.env.NODE_ENV === 'production';

const dataPath = path.join(__dirname, 'data', 'keyboards.json');
const keyboards = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
console.log(`[server] loaded ${keyboards.length} keyboards from ${dataPath}`);

const app = express();

app.use(
  cors({
    origin: isProd ? false : ['http://localhost:5173'],
  })
);

app.get('/api/health', (_req, res) => {
  res.json({ ok: true, count: keyboards.length });
});

app.get('/api/keyboards', (_req, res) => {
  res.json(keyboards);
});

if (isProd) {
  const clientDist = path.resolve(__dirname, '..', 'client', 'dist');
  app.use(express.static(clientDist));
  app.get('*', (_req, res) => {
    res.sendFile(path.join(clientDist, 'index.html'));
  });
}

app.listen(PORT, () => {
  console.log(`[server] listening on http://localhost:${PORT}`);
});
