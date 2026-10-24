-- Runs once when the Postgres container is first created.
CREATE TABLE IF NOT EXISTS items (
    id    SERIAL PRIMARY KEY,
    name  TEXT    NOT NULL,
    price NUMERIC NOT NULL CHECK (price > 0)
);

INSERT INTO items (name, price) VALUES
    ('Notebook', 3.50),
    ('Pen', 1.50);
