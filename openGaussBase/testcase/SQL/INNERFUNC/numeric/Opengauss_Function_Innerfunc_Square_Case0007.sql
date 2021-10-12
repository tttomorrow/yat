-- @testpoint: 数字操作符|/(平方根),数据为1或者最大值时进行开方
drop table if exists data_01;
create table data_01 (clo1 int,clo2 BIGINT);
select |/clo1,|/clo2 from data_01;
drop table if exists data_01;