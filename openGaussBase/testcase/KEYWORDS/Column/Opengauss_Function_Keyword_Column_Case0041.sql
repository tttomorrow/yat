--  @testpoint:删除表字段，不带column字段
drop table if exists yy;
create table yy(id int);
alter table yy add ( age int,t_name char(20));
alter table yy drop  age;
drop table yy;