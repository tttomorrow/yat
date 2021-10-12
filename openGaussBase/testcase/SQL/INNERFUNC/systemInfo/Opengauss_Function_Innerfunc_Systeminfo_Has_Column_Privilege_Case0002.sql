-- @testpoint: 给表的某一列赋予权限查询该列是否有此权限（当列的参数为smallint）
DROP USER IF EXISTS joe CASCADE;
CREATE USER joe PASSWORD 'Bigdata@123';
DROP table IF EXISTS table_test001;
create table table_test001(c int,d int); 
GRANT select (c),update (d) ON table_test001 TO joe;
SELECT has_column_privilege('joe', 'table_test001',1:: smallint ,'select');
DROP USER IF EXISTS joe CASCADE;
DROP table IF EXISTS table_test001;