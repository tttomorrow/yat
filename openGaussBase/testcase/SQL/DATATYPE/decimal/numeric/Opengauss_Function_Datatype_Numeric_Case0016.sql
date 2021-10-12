-- @testpoint: 指定精度在合理范围值内，插入数据超出精度设定值，合理报错
-- @modified at: 2020-11-23

drop table if exists numeric_16;
create table numeric_16 (name numeric(6,2));
insert into numeric_16 values (12345.123456);
insert into numeric_16 values (99999.99);
insert into numeric_16 values (100000);
drop table numeric_16;