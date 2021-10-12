-- @testpoint: 给表赋予权限当权限参数privilege正确的时候查询
DROP USER IF EXISTS joe CASCADE;
CREATE USER joe PASSWORD 'Bigdata@123';
DROP table IF EXISTS table_test001;
create table table_test001(c int,d int); 
GRANT select,update ON table_test001 TO joe;
SELECT has_table_privilege('joe', 'table_test001','select');
DROP USER IF EXISTS joe CASCADE;
DROP table IF EXISTS table_test001;