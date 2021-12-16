-- @testpoint: 数字操作符^(幂),指数运算超出最大值，合理报错
drop table if exists data_01;
create table data_01 (clo1 BIGINT,clo2 BIGINT);
insert into data_01 values (9223372036854775806, 2);
select clo1 * clo2 from data_01;
SELECT -9223372036854775806 * 2 AS RESULT;
drop table if exists data_01;