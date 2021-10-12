-- @testpoint: 插入浮点数

drop table if exists serial_03;
create table serial_03 (name serial);
insert into serial_03 values (12122.12);
insert into serial_03 values (0.0000001);
insert into serial_03 values (-12122.23);
insert into serial_03 values (-0.0000001);
select * from serial_03;
drop table serial_03;
