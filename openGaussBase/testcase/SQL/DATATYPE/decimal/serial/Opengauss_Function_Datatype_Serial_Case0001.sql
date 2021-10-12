-- @testpoint: 插入正整数

drop table if exists serial_01;
create table serial_01 (name serial);
insert into serial_01 values (120);
insert into serial_01 values (99999);
insert into serial_01 values (1);
insert into serial_01 values (2);
insert into serial_01 values (3);
select * from serial_01;
drop table serial_01;