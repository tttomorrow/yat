-- @testpoint: octet_length函数入参为变长类型字符串
drop  table  if exists products;
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
select octet_length(product_name),octet_length(category)from products;
drop  table  if exists products;