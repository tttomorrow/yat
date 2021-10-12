-- @testpoint: 插入字符串形式整数

drop table if exists serial_04;
create table serial_04 (name serial);
insert into serial_04 values ('132');
insert into serial_04 values ('9999999');
insert into serial_04 values ('-132');
insert into serial_04 values ('-9999999');
select * from serial_04;
drop table serial_04;
