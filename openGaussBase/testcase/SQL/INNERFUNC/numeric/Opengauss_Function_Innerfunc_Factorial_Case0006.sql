-- @testpoint: 数字操作符!(阶乘),阶乘结果过大溢出，合理报错
drop table if exists data_01;
create table data_01 (clo1 BIGINT,clo2 BIGINT);
insert into data_01 values (922337036854775807, 9223372036854775807);
select  clo1! from data_01;
select  clo2! from data_01;
drop table if exists data_01;