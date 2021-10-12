-- @testpoint: 将表中字段的查询权限赋予指定的用户或角色

drop user if exists user_007 cascade;
create user user_007 identified by 'Gauss_234';

drop table if exists t7;
create table t7(id int ,name char(255),age int ,city varchar (255));
grant select (id,name) on t7 to user_007;
-- set search_path to user_007;
-- select id,name FROM t7;
revoke select on t7 from user_007;

drop table if exists t7;
drop user if exists user_007;

