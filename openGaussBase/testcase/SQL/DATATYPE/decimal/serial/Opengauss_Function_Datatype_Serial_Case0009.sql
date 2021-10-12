-- @testpoint: 插入字符串类型数值

drop table if exists serial_09;
create table serial_09 (name serial);
insert into serial_09 values ('12354563');
insert into serial_09 values ('-12354563');
insert into serial_09 values ('1');
insert into serial_09 values ('-1');
select * from serial_09;
drop table serial_09;