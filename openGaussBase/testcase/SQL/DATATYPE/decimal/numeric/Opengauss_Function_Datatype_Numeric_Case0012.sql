-- @testpoint: 插入非法空值，合理报错

drop table if exists numeric_12;
create table numeric_12 (id int,name numeric);
insert into numeric_12 values (1,' ');
drop table numeric_12;