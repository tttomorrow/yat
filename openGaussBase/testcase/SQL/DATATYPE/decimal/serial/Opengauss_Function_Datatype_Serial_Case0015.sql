-- @testpoint: 插入default自定义值

drop table if exists serial_15;
create table serial_15 (name serial);
insert into serial_15 values (default);
insert into serial_15 values (default);
insert into serial_15 values (default);
insert into serial_15 values (default);
insert into serial_15 values (default);
select * from serial_15;
drop table serial_15;