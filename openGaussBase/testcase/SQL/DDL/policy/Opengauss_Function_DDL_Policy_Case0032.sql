--  @testpoint:不同数据表，支持创建同名的行访问控制策略，成功
--创建表1
drop table if exists products;
CREATE TABLE products(product_id INTEGER,product_name VARCHAR2(60),category VARCHAR2(60));
INSERT INTO products VALUES (1501, 'vivitar 35mm', 'electrncs');
--创建表2
drop table if exists  newproducts;
CREATE TABLE newproducts(product_id INTEGER,product_name VARCHAR2(60),category VARCHAR2(60));
INSERT INTO newproducts VALUES (1502, 'olympus camera', 'electrncs');
--表1创建行访问控制策略test_pol1
drop POLICY if exists test_pol1 ON products;
CREATE POLICY test_pol1 ON products FOR select TO PUBLIC USING (product_id = 1501);
--表2创建同名行访问控制策略test_pol1
drop POLICY if exists test_pol1 ON newproducts;
CREATE POLICY test_pol1 ON newproducts FOR select TO PUBLIC USING (product_id = 1502);
--删除行访问控制策略
drop POLICY test_pol1 ON products;
drop POLICY test_pol1 ON newproducts;
--删除表
drop table products;
drop table newproducts;