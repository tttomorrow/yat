-- @testpoint: 给表赋予所有权限的时候查询是否有某一列的权限
DROP USER IF EXISTS joe CASCADE;
CREATE USER joe PASSWORD 'Bigdata@123';
DROP table IF EXISTS table_test001;
create table table_test001(c int,d int); 
GRANT ALL PRIVILEGES ON table_test001 TO joe;
SELECT has_column_privilege('joe', 'table_test001','c' ,'insert');
SELECT has_column_privilege('joe', 'table_test001',1:: smallint ,'update');
SELECT has_column_privilege('joe', 'table_test001',2:: smallint ,'select');
DROP USER IF EXISTS joe CASCADE;
DROP table IF EXISTS table_test001;