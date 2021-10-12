-- @testpoint: 插入非法空值,合理报错

drop table if exists serial_12;
create table serial_12 (id int,name serial);
insert into serial_12 values (1,' ');
drop table serial_12;