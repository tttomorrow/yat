-- @testpoint: 插入bool类型

drop table if exists serial_10;
create table serial_10 (name serial);
insert into serial_10 values (false);
insert into serial_10 values (true);
select * from serial_10;
drop table serial_10;