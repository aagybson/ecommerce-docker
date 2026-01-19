CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name TEXT,
  category TEXT,
  price NUMERIC
);

INSERT INTO products (name, category, price) VALUES
('Laptop', 'electronics', 1200),
('Phone', 'electronics', 800),
('TV', 'electronics', 1500),
('Chair', 'furniture', 150),
('Table', 'furniture', 300),
('Sofa', 'furniture', 900),
('Shirt', 'clothing', 40),
('Jeans', 'clothing', 60),
('Jacket', 'clothing', 120),
('Shoes', 'clothing', 90);

