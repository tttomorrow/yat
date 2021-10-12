-- @testpoint: 将表空间的访问权限赋予指定的用户或角色

drop user if exists user_015 cascade;
create user user_015 identified by 'Gauss_234';
drop tablespace if exists tbspc;
create tablespace tbspc relative location 'tablespace/tablespace_111';
grant all on tablespace tbspc to user_015;

--回收权限
revoke all privileges on tablespace tbspc from user_015;
drop tablespace if exists tbspc;
drop user if exists user_015;

