-- @testpoint: 通过role_id检查用户是否存在
DROP ROLE IF EXISTS manager;
CREATE ROLE manager IDENTIFIED BY 'Bigdata@123';
select pg_check_authid(oid) from pg_roles  where rolname ='manager' ;
DROP ROLE IF EXISTS manager;
