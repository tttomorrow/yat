-- @testpoint: 指定精度在合理范围值内，插入数据超出精度设定值，合理报错

drop table if exists decimal_16;
create table decimal_16 (name decimal(6,2));
insert into decimal_16 values (123456.123456);
insert into decimal_16 values (99999.99);
insert into decimal_16 values (100000);
drop table decimal_16;