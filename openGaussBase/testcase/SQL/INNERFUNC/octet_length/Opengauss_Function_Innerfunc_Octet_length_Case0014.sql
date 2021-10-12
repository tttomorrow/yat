-- @testpoint: octet_length函数与insert结合使用
drop  table if exists products;
CREATE TABLE products
( product_id INTEGER,
  product_name VARCHAR2(60),
  category VARCHAR2(60)
);
INSERT INTO products VALUES
(1699,'lilei',octet_length('sfkj^&**(00//')),
(1699,'lilei',octet_length('sjd很快就士大夫'));
drop table products;