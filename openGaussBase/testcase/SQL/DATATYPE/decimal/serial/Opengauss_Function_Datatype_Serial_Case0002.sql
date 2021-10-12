-- @testpoint: 插入负整数

drop table if exists serial_02;
create table serial_02 (name serial);
insert into serial_02 values (-1212);
insert into serial_02 values (-99999999);
insert into serial_02 values (-1);
insert into serial_02 values (-2);
insert into serial_02 values (-3);
select * from serial_02;
drop table serial_02;
