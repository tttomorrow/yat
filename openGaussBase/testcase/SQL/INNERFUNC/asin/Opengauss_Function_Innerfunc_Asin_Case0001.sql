-- @testpoint: 与insert into结合的边界值使用
drop table if exists asin_test_01;
create table asin_test_01(c_decimal decimal(38,4));
insert into asin_test_01(c_decimal) values(-1),(1),(-0.6542),(1.01),(-1.01),(0.6542),(null);
select asin(c_decimal) t1 from asin_test_01 where c_decimal in (1,-1) order by t1;
drop table if exists asin_test_01;
