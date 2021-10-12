-- @testpoint: role参数为role oid时有角色权限和没有角色权限返回值校验
DROP USER IF EXISTS senior_manager CASCADE;
DROP ROLE IF EXISTS manager;
CREATE ROLE manager IDENTIFIED BY 'Bigdata@123';
CREATE USER senior_manager PASSWORD 'Bigdata@123';
select pg_has_role('senior_manager', oid, 'USAGE') from PG_AUTHID where rolname = 'manager';
GRANT manager TO senior_manager WITH ADMIN OPTION;
select pg_has_role('senior_manager', oid, 'USAGE') from PG_AUTHID where rolname = 'manager';
DROP ROLE IF EXISTS manager;
DROP USER IF EXISTS senior_manager CASCADE;