-- @testpoint: 与distinct函数结合使用
DROP TABLE IF EXISTS products;
CREATE TABLE products
( product_id INTEGER,
  product_name VARCHAR2(60),
  category VARCHAR2(60)
);
INSERT INTO products VALUES(1502, 'olympus camera', 'electrncs');
INSERT INTO products VALUES(1601, 'lamaze', 'toys');
select distinct product_name  from products;
DROP TABLE IF EXISTS products;