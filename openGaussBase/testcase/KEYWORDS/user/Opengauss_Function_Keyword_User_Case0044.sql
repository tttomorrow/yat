-- @testpoint: 添加、修改、删除user列
drop table if exists user_05;
create table user_05 (name varchar(13),school varchar(13));
alter table user_05 add "user" char(10);
update user_05 set "user"='aa';
alter table user_05 drop "user";
drop table if exists user_05;