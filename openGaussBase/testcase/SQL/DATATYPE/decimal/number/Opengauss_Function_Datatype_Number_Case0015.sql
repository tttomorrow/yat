-- @testpoint: 指定精度在合理范围值内，插入数据
-- @modified at: 2020-11-23

drop table if exists number_15;
create table number_15 (name number(6,2));
insert into number_15 values (123.12);
insert into number_15 values (1234.12);
insert into number_15 values (1234.1234);
insert into number_15 values (9999.99);
select * from number_15;
drop table number_15;