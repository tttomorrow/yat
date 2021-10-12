-- @testpoint: 插入非法空值,合理报错

drop table if exists int08;
create table int08 (id int,name int);
insert into int08 values (1,' ');
drop table int08;