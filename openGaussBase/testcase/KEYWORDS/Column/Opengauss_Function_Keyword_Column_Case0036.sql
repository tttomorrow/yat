--  @testpoint:给表添加一个字段,使用add...column
drop table if exists yy;
create table yy(id int);
alter table yy add column age int;
drop table yy;
------给表添加一个字段,使用add，不加column选项

drop table if exists yy;
create table yy(id int);
alter table yy add  age int;
drop table yy;