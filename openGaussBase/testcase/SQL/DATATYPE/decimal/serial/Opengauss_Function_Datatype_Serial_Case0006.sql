-- @testpoint: 插入超出左边界范围值，隐式转换integer

drop table if exists serial_06;
create table serial_06 (name serial);
insert into serial_06 values (0);
select * from serial_06;
drop table serial_06;