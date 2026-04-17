import path from 'node:path';
import { fileURLToPath } from 'node:url';
import Database from 'better-sqlite3';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DB_PATH = path.resolve(__dirname, '..', 'data', 'keyboards.db');

let db;
export function openDb() {
  if (db) return db;
  db = new Database(DB_PATH, { readonly: false });
  db.pragma('foreign_keys = ON');
  return db;
}

// --- Taxonomy ---

export function getTaxonomy() {
  const d = openDb();

  const attrTypes = d
    .prepare(
      'SELECT id, key, label, multi FROM attribute_types ORDER BY display_order, id'
    )
    .all();
  const attrValsByType = new Map();
  for (const row of d
    .prepare(
      'SELECT attribute_type_id, value FROM attribute_values ORDER BY display_order, id'
    )
    .all()) {
    if (!attrValsByType.has(row.attribute_type_id)) attrValsByType.set(row.attribute_type_id, []);
    attrValsByType.get(row.attribute_type_id).push(row.value);
  }

  const compTypes = d
    .prepare(
      'SELECT id, key, label FROM component_types ORDER BY display_order, id'
    )
    .all();
  const brandsByType = new Map();
  for (const row of d
    .prepare(
      'SELECT component_type_id, label, aliases FROM brand_tags ORDER BY display_order, id'
    )
    .all()) {
    if (!brandsByType.has(row.component_type_id)) brandsByType.set(row.component_type_id, []);
    brandsByType.get(row.component_type_id).push({
      label: row.label,
      aliases: row.aliases ? JSON.parse(row.aliases) : [row.label.toLowerCase()],
    });
  }

  return {
    attribute_types: attrTypes.map((at) => ({
      key: at.key,
      label: at.label,
      multi: !!at.multi,
      values: attrValsByType.get(at.id) || [],
    })),
    component_types: compTypes.map((ct) => ({
      key: ct.key,
      label: ct.label,
      brand_tags: brandsByType.get(ct.id) || [],
    })),
  };
}

// --- Keyboards ---

function hydrate(d, rows) {
  if (rows.length === 0) return [];
  const ids = rows.map((r) => r.id);
  const placeholders = ids.map(() => '?').join(',');

  const byId = new Map(
    rows.map((r) => [
      r.id,
      {
        id: r.id,
        title: r.title,
        author: r.author,
        permalink: r.permalink,
        created_utc: r.created_utc,
        score: r.score,
        thumbnail_url: r.thumbnail_url,
        confidence: r.confidence,
        image_urls: [],
        components: {},
        component_brands: {},
        attributes: {},
        raw: { selftext: null, parts_source_text: null },
      },
    ])
  );

  for (const row of d
    .prepare(
      `SELECT keyboard_id, selftext, parts_source_text FROM keyboard_raw WHERE keyboard_id IN (${placeholders})`
    )
    .all(...ids)) {
    const kb = byId.get(row.keyboard_id);
    kb.raw.selftext = row.selftext;
    kb.raw.parts_source_text = row.parts_source_text;
  }

  for (const row of d
    .prepare(
      `SELECT keyboard_id, url FROM images WHERE keyboard_id IN (${placeholders}) ORDER BY idx`
    )
    .all(...ids)) {
    byId.get(row.keyboard_id).image_urls.push(row.url);
  }

  // Seed empty shapes from taxonomy so consumers always see every slot.
  const compTypes = d.prepare('SELECT id, key FROM component_types').all();
  const compKeyById = new Map(compTypes.map((r) => [r.id, r.key]));
  for (const kb of byId.values()) {
    for (const ct of compTypes) {
      kb.components[ct.key] = null;
      kb.component_brands[ct.key] = [];
    }
  }
  const attrTypes = d.prepare('SELECT id, key FROM attribute_types').all();
  const attrKeyByValueId = new Map(
    d
      .prepare(
        'SELECT av.id AS value_id, at.key AS key, av.value AS value FROM attribute_values av JOIN attribute_types at ON at.id = av.attribute_type_id'
      )
      .all()
      .map((r) => [r.value_id, { key: r.key, value: r.value }])
  );
  for (const kb of byId.values()) {
    for (const at of attrTypes) kb.attributes[at.key] = [];
  }

  for (const row of d
    .prepare(
      `SELECT keyboard_id, component_type_id, text FROM keyboard_components WHERE keyboard_id IN (${placeholders})`
    )
    .all(...ids)) {
    const kb = byId.get(row.keyboard_id);
    kb.components[compKeyById.get(row.component_type_id)] = row.text;
  }

  const brandByTagId = new Map(
    d
      .prepare(
        'SELECT bt.id AS bid, bt.label AS label, bt.component_type_id AS ctid FROM brand_tags bt'
      )
      .all()
      .map((r) => [r.bid, { label: r.label, ctid: r.ctid }])
  );
  for (const row of d
    .prepare(
      `SELECT keyboard_id, brand_tag_id FROM keyboard_brand_tags WHERE keyboard_id IN (${placeholders})`
    )
    .all(...ids)) {
    const b = brandByTagId.get(row.brand_tag_id);
    if (!b) continue;
    const kb = byId.get(row.keyboard_id);
    kb.component_brands[compKeyById.get(b.ctid)].push(b.label);
  }

  for (const row of d
    .prepare(
      `SELECT keyboard_id, attribute_value_id FROM keyboard_attributes WHERE keyboard_id IN (${placeholders})`
    )
    .all(...ids)) {
    const av = attrKeyByValueId.get(row.attribute_value_id);
    if (!av) continue;
    byId.get(row.keyboard_id).attributes[av.key].push(av.value);
  }

  return rows.map((r) => byId.get(r.id));
}

export function getAllKeyboards() {
  const d = openDb();
  const rows = d
    .prepare(
      'SELECT id, title, author, permalink, created_utc, score, thumbnail_url, confidence FROM keyboards ORDER BY score DESC'
    )
    .all();
  return hydrate(d, rows);
}

export function getKeyboardById(id) {
  const d = openDb();
  const row = d
    .prepare(
      'SELECT id, title, author, permalink, created_utc, score, thumbnail_url, confidence FROM keyboards WHERE id = ?'
    )
    .get(id);
  if (!row) return null;
  return hydrate(d, [row])[0];
}

export function countKeyboards() {
  return openDb().prepare('SELECT COUNT(*) AS n FROM keyboards').get().n;
}
