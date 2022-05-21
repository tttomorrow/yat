-- @testpoint: 指定精度在合理范围值内，插入数据
-- @modified at: 2020-11-23

drop table if exists numeric_15;
create table numeric_15 (name numeric(6,2));
insert into numeric_15 values (123.12);
insert into numeric_15 values (1234.12);
insert into numeric_15 values (1234.1234);
insert into numeric_15 values (9999.99);
insert into numeric_15 values (1.11223344566);
select * from numeric_15;
drop table numeric_15;