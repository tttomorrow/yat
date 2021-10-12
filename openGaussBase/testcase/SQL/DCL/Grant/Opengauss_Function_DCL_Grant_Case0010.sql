-- @testpoint: 将表中字段的删除权限赋予指定的用户或角色

drop user if exists user_010 cascade;
create user user_010 identified by 'Gauss_234';

drop table if exists t10;
create table t10(id int ,name char(255),age int ,city varchar (255));

grant delete on t10 to user_010;
revoke delete on t10 from user_010;

drop table if exists t10;
drop user if exists user_010;