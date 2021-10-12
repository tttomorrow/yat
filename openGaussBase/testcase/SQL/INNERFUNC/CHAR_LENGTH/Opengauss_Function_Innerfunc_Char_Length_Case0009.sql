-- @testpoint: char_length函数与order by结合测试
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
select char_length(product_name)from products order by product_id;
drop table  if exists products;