-- @testpoint: 插入非法空值，合理报错

drop table if exists float12;
create table float12 (id int,name float);
insert into float12 values (1,' ');
drop table float12;