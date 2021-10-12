-- @testpoint: 数字操作符@(绝对值)，数值0求绝对值
drop table if exists data_01;
create table data_01 (clo1 BIGINT,clo2 BIGINT);
insert into data_01 values (0, 2);
select @clo1 from data_01;
SELECT @0 AS RESULT;
drop table if exists data_01;