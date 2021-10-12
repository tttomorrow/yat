-- @testpoint: 给表user_01添加user列
drop table if  exists user_01;
create table user_01 (name varchar(13),school varchar(13));
alter table user_01 add "user" char(3);
drop table if  exists user_01;