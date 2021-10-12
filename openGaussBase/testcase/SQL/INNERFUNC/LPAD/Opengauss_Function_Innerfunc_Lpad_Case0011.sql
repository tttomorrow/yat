-- @testpoint: lpad函数与order by结合使用
drop  table  if exists products ;
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
(1677,'hemai','liulaoshizi');
select product_name from products order by lpad(category,15,'sister');
drop  table  if exists products ;