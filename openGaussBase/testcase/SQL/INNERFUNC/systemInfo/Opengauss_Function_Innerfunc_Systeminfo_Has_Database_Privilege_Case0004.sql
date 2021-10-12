-- @testpoint: 数据库参数为数据库oid时有权限和无权限时返回值校验
DROP USER IF EXISTS joe CASCADE;
CREATE USER joe PASSWORD 'Bigdata@123';
DROP database IF EXISTS dbtest_001;
create database dbtest_001; 
GRANT connect on database dbtest_001 TO joe ;
select has_database_privilege('joe',oid, 'create' ) from PG_DATABASE where datname = 'dbtest_001';
select has_database_privilege('joe',oid, 'connect' ) from PG_DATABASE where datname = 'dbtest_001';
DROP USER IF EXISTS joe CASCADE;
DROP database IF EXISTS dbtest_001;