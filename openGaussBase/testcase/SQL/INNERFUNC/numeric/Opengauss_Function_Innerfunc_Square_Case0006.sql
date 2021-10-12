-- @testpoint: 数字操作符|/(平方根),负数进行开方，合理报错
drop table if exists data_01;
create table data_01 (clo1 int,clo2 int);
insert into data_01 values (-125, -126);
select |/clo1 from data_01;
SELECT |/ -16 AS RESULT;
drop table if exists data_01;