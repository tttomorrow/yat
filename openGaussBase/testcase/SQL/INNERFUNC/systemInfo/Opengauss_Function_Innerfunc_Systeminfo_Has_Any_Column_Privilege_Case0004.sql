-- @testpoint: 当表参数为表oid时，表中任意一列有权限和没有权限时返回值校验
DROP USER IF EXISTS joe CASCADE;
CREATE USER joe PASSWORD 'Bigdata@123';
DROP table IF EXISTS table_test001;
create table table_test001(c int,d int); 
GRANT select (c),update (d) ON table_test001 TO joe;
select has_any_column_privilege('joe', oid,'select') from PG_CLASS where relname = 'table_test001' ;
select has_any_column_privilege('joe', oid,'insert') from PG_CLASS where relname = 'table_test001' ;
DROP USER IF EXISTS joe CASCADE;
DROP table IF EXISTS table_test001;