-- @testpoint: 改变表字段的数据类型,不带column
drop table if exists yy;
create table yy(id int);
alter table yy add ( age int,t_name char(20));
ALTER TABLE yy ALTER  t_name TYPE varchar(2);
drop table if exists yy;