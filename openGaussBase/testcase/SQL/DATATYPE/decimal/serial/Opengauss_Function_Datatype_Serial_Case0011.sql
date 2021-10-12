-- @testpoint: 插入指数形式值

drop table if exists serial_11;
create table serial_11 (name serial);
insert into serial_11 values (exp(12));
insert into serial_11 values (exp(1.23));
insert into serial_11 values (exp(-15));
insert into serial_11 values (exp(-1.5));
select * from serial_11;
drop table serial_11;