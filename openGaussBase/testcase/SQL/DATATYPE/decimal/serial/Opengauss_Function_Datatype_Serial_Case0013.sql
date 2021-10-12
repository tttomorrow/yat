-- @testpoint: 插入0值

drop table if exists serial_13;
create table serial_13 (name serial);
insert into serial_13 values (0);
insert into serial_13 values (0);
insert into serial_13 values (0);
select * from serial_13;
drop table serial_13;