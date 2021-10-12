-- @testpoint: 给表的赋予所有权限参数查询是否具有正确权限
DROP USER IF EXISTS joe CASCADE;
CREATE USER joe PASSWORD 'Bigdata@123';
DROP table IF EXISTS table_test001;
create table table_test001(c int,d int); 
GRANT ALL PRIVILEGES ON table_test001 TO joe;
SELECT has_any_column_privilege('joe', 'table_test001','INSERT');
DROP USER IF EXISTS joe CASCADE;
DROP table IF EXISTS table_test001;