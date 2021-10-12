--  @testpoint:创建行访问控制策略，指定行访问控制SQL操作为merge into,合理报错
--创建目标表
drop table if exists products;
CREATE TABLE products(product_id INTEGER,product_name VARCHAR2(60),category VARCHAR2(60));
INSERT INTO products VALUES (1501, 'vivitar 35mm', 'electrncs');
--创建源表
drop table if exists  newproducts;
CREATE TABLE newproducts(product_id INTEGER,product_name VARCHAR2(60),category VARCHAR2(60));
INSERT INTO newproducts VALUES (1502, 'olympus camera', 'electrncs');
--打开行级安全检查
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE newproducts ENABLE ROW LEVEL SECURITY;
--创建测试用户
drop user if exists s_usr1 cascade;
create user s_usr1 password 'Test@123';
--授予用户表的所有权限
grant all on products to s_usr1;
--创建策略,指定行访问控制影响的数据库用户为public,sql操作为merge into,合理报错，merge into策略不能具有using_expression
drop POLICY if exists pol1 ON products;
CREATE POLICY pol1 ON products FOR merge into TO PUBLIC USING (product_id = 1501);
--删除表
drop table products;
drop table newproducts;
--删除用户
drop user s_usr1 cascade;

