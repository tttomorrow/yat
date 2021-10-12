-- @testpoint: pg_stat_get_role_name(oid)根据用户oid获取用户名
-- testpoint：测试当前用户
select pg_stat_get_role_name(10) = CURRENT_USER;
select pg_stat_get_role_name(10) = CURRENT_ROLE;
-- testpoint：新建用户名普通的用户
DROP USER if exists kim;
CREATE USER kim IDENTIFIED BY 'Bigdata@123';
select pg_stat_get_role_name(a.oid) from PG_ROLES a where a.rolname = 'kim';
DROP USER kim CASCADE;
-- testpoint：新建用户名是最大长度以下滑线开头的用户
DROP USER if exists ___abcd5abcd5abcd5abcd5abcd5abcd5abcd5abcd5abcd5abcd5abcd5abcd5;
CREATE USER ___abcd5abcd5abcd5abcd5abcd5abcd5abcd5abcd5abcd5abcd5abcd5abcd5 IDENTIFIED BY 'Bigdata@123';
select pg_stat_get_role_name(a.oid) from PG_ROLES a where a.rolname = '___abcd5abcd5abcd5abcd5abcd5abcd5abcd5abcd5abcd5abcd5abcd5abcd5';
DROP USER ___abcd5abcd5abcd5abcd5abcd5abcd5abcd5abcd5abcd5abcd5abcd5abcd5 CASCADE;
