-- @testpoint: 将表中字段的插入权限赋予指定的用户或角色

drop user if exists user_008 cascade;
create user user_008 identified by 'Gauss_234';

drop table if exists t8;
create table t8(id int ,name char(255),age int ,city varchar (255));

grant insert on t8 to user_008;
revoke insert on t8 from user_008;

drop table if exists t8;
drop user if exists user_008;
