'use client';

import { useEffect, useState } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

type Item = { id: number; name: string; price: number };

export default function Home() {
  const [items, setItems] = useState<Item[]>([]);
  const [name, setName] = useState('');
  const [price, setPrice] = useState('');
  const [error, setError] = useState('');

  async function load() {
    try {
      const res = await fetch(`${API_URL}/items`);
      setItems(await res.json());
    } catch {
      setError('Could not reach the API. Is the stack up?');
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function addItem(e: React.FormEvent) {
    e.preventDefault();
    setError('');
    const res = await fetch(`${API_URL}/items`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, price: Number(price) }),
    });
    if (res.ok) {
      setName('');
      setPrice('');
      load();
    } else {
      setError('Item rejected (name required, price must be > 0).');
    }
  }

  return (
    <main style={{ maxWidth: 560, margin: '3rem auto', fontFamily: 'system-ui' }}>
      <h1>Items</h1>
      <p>FastAPI + PostgreSQL + Next.js, running in Docker Compose.</p>

      <form onSubmit={addItem} style={{ display: 'flex', gap: 8, margin: '1rem 0' }}>
        <input
          placeholder="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          placeholder="price"
          type="number"
          step="0.01"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
          required
        />
        <button type="submit">Add</button>
      </form>

      {error && <p style={{ color: 'crimson' }}>{error}</p>}

      <ul>
        {items.map((it) => (
          <li key={it.id}>
            {it.name} — ${it.price.toFixed(2)}
          </li>
        ))}
      </ul>
    </main>
  );
}
