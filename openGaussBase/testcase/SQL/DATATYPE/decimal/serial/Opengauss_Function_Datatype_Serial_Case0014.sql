-- @testpoint: 插入空值,合理报错

drop table if exists serial_14;
create table serial_14 (id int,name serial);
insert into serial_14 values (1,null);
insert into serial_14 values (2,'');
drop table serial_14;