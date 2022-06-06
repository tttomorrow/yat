-- @testpoint: 指定精度在合理范围值内，插入数据
-- @modified at: 2020-11-23

drop table if exists decimal_15;
create table decimal_15 (name decimal(6,2));
insert into decimal_15 values (123.12);
insert into decimal_15 values (1234.12);
insert into decimal_15 values (1234.1234);
insert into decimal_15 values (9999.99);
insert into decimal_15 values (1.11223344566);
select * from decimal_15;
drop table decimal_15;