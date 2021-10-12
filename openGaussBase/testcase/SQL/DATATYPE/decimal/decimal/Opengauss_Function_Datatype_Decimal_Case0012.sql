-- @testpoint: 插入非法空值，合理报错

drop table if exists decimal_12;
create table decimal_12 (id int,name decimal);
insert into decimal_12 values (1,' ');
drop table decimal_12;