-- @testpoint:  ALTER DEFAULT PRIVILEGES（目前只支持表（包括视图）、 函数和类型（包括域）的权限更改。）

--将创建在模式test里的所有表（和视图）的SELECT权限授予每一个用户。
drop schema if exists test ;
create schema test;

alter default privileges in schema test grant select on tables to public;
--撤销上述权限
alter default privileges in schema test revoke select on tables from public;

--将test下的所有表的插入权限授予用户user_020。
drop user if exists user_020 cascade;
create user user_020 identified by 'Gauss_234';

alter default privileges in schema test grant insert on tables to user_020;
--撤销上述权限
alter default privileges in schema test revoke insert on tables from user_020;

drop schema test;
drop user if exists user_020;