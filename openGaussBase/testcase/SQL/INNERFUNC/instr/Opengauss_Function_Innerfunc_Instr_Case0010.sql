-- @testpoint: instr函数在查询语句中与distinct结合
--建表
drop table if exists products;
CREATE TABLE products
( product_id INTEGER,
  product_name VARCHAR2(60),
  category VARCHAR2(60)
);
--插入数据
INSERT INTO products VALUES
(1502, 'olympus camera', 'electrncs'),
(1601, 'lamaze', 'toys'),
(1666, 'harry potter', 'toys'),
(1700, 'wait interface', 'books'),
(1702,'luoen','time'),
(1672,'hemai','hogwarzi'),
(1677,'hemai','liulaoshizi');
--查询
select distinct(product_name) from  products where instr(category,'warzi',2,1)=4;
--清理环境
drop table if exists products;
