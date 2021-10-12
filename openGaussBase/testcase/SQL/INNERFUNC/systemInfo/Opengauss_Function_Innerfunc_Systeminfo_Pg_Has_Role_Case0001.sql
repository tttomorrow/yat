-- @testpoint: role存在某项权限返回为true
DROP USER IF EXISTS senior_manager CASCADE;
DROP ROLE IF EXISTS manager;
CREATE ROLE manager IDENTIFIED BY 'Bigdata@123';
CREATE USER senior_manager PASSWORD 'Bigdata@123';
GRANT manager TO senior_manager;
select pg_has_role('senior_manager', 'manager', 'USAGE');
DROP ROLE IF EXISTS manager;
DROP USER IF EXISTS senior_manager CASCADE;