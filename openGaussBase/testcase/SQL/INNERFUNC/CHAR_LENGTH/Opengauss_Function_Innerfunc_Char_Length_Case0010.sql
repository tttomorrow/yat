-- @testpoint: char_length函数与where 条件结合使用
drop table  if exists products;
CREATE TABLE products
( product_id INTEGER,
  product_name VARCHAR2(60),
  category VARCHAR2(60)
);
INSERT INTO products VALUES
(1502, 'olympus camera', 'electrncs'),
(1601, 'lamaze', 'toys'),
(1666, 'harry potter', 'toys'),
(1700, 'wait interface', 'books'),
(1702,'luoen','time'),
(1672,'hemai','hogwarzi'),
(1677,'hemai','hoi');
select  category from products where char_length(product_name) =6;
drop table  if exists products;