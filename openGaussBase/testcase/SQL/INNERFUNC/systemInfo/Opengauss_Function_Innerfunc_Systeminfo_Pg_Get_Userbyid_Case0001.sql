-- @testpoint: 获取给定OID的角色名
DROP ROLE IF EXISTS manager;
CREATE ROLE manager IDENTIFIED BY 'Bigdata@123';
select pg_get_userbyid(oid) from pg_roles  where rolname ='manager' ;
DROP ROLE IF EXISTS manager;
