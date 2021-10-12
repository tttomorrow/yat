-- @testpoint: 将表中字段的更新权限赋予指定的用户或角色

drop user if exists user_009 cascade;
create user user_009 identified by 'Gauss_234';

drop table if exists t9;
create table t9(id int ,name char(255),age int ,city varchar (255));

grant update on t9 to user_009;
revoke update on t9 from user_009;

drop table if exists t9;
drop user if exists user_009;
