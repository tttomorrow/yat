-- @testpoint: 插入超出右边界范围值，合理报错

drop table if exists serial_07;
create table serial_07 (name serial);
drop table serial_07;
