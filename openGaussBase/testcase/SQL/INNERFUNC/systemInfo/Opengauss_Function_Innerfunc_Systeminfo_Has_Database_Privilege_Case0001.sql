-- @testpoint: 给数据库的任意一项权限时查询该权限是否存在
DROP USER IF EXISTS joe CASCADE;
CREATE USER joe PASSWORD 'Bigdata@123';
DROP database IF EXISTS dbtest_001;
create database dbtest_001; 
GRANT create,connect on database dbtest_001 TO joe ;
SELECT has_database_privilege('joe', 'dbtest_001','connect');
DROP USER IF EXISTS joe CASCADE;
DROP database IF EXISTS dbtest_001;