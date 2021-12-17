-- @testpoint: 插入右边界范围值

drop table if exists serial_08;
create table serial_08 (name serial);
insert into serial_08 values (2147483647);
select * from serial_08;
drop table serial_08;