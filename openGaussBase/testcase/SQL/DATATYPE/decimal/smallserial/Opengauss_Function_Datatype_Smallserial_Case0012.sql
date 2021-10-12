-- @testpoint: 插入非法空值，合理报错

drop table if exists smallserial_12;
create table smallserial_12 (id int,name smallserial);
insert into smallserial_12 values (1,' ');
drop table smallserial_12;