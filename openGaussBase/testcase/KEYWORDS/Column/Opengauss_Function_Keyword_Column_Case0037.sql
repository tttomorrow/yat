--  @testpoint:给表添加多个字段，不带column
drop table if exists yy;
create table yy(id int);
alter table yy add ( age1 int,t_name char(20));
drop table yy;