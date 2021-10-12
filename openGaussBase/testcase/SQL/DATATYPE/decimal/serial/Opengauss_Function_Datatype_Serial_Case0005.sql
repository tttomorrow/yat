-- @testpoint: 插入左边界范围值

drop table if exists serial_05;
create table serial_05 (name serial);
insert into serial_05 values (1);
select * from serial_05;
drop table serial_05;