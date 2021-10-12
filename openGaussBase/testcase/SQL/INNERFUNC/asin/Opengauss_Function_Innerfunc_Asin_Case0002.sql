-- @testpoint: 输入在[-1,1]范围内
drop table if exists asin_test_02;
create table asin_test_02(c_decimal decimal(38,4));
insert into asin_test_02(c_decimal) values(-1),(1),(-0.6542),(0.6542),(null);
select asin(c_decimal) from asin_test_02 where c_decimal not in (1,-1);
drop table if exists asin_test_02;