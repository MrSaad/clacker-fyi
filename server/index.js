import express from 'express';
import cors from 'cors';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  getAllKeyboards,
  getKeyboardById,
  getTaxonomy,
  countKeyboards,
} from './db.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PORT = process.env.PORT || 3001;
const isProd = process.env.NODE_ENV === 'production';

const app = express();
app.use(cors({ origin: isProd ? false : ['http://localhost:5173'] }));

app.get('/api/health', (_req, res) => {
  res.json({ ok: true, count: countKeyboards() });
});

app.get('/api/keyboards', (_req, res) => {
  res.json(getAllKeyboards());
});

app.get('/api/keyboards/:id', (req, res) => {
  const kb = getKeyboardById(req.params.id);
  if (!kb) return res.status(404).json({ error: 'not found' });
  res.json(kb);
});

app.get('/api/taxonomy', (_req, res) => {
  res.json(getTaxonomy());
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
