--  @testpoint:删除表字段，带column
drop table if exists yy;
create table yy(id int);
alter table yy add ( age int,t_name char(20));
alter table yy drop column age;
drop table yy;