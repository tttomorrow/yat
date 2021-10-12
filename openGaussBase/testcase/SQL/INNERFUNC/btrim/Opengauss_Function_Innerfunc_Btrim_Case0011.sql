-- @testpoint: 与distinct函数结合使用
DROP TABLE IF EXISTS products;
CREATE TABLE products
( product_id INTEGER,
  product_name VARCHAR2(60),
  category VARCHAR2(60)
);

INSERT INTO products VALUES(1502, 'olympus camera', 'great openGauss');
INSERT INTO products VALUES(1601, 'lamaze', 'openGauss  great');
INSERT INTO products VALUES(1601, 'lamaze', 'openGauss  great');
select distinct product_id  from products where btrim(category,' tearg')='openGauss';
DROP TABLE IF EXISTS products;