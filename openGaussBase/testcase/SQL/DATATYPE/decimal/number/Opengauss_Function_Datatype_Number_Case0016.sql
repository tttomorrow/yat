-- @testpoint: 指定精度在合理范围值内，插入数据超出精度设定值，合理报错
-- @modified at: 2020-11-23

drop table if exists number_16;
create table number_16 (name number(6,2));
insert into number_16 values (12345.123456);
insert into number_16 values (99999.99);
insert into number_16 values (100000);
drop table number_16;