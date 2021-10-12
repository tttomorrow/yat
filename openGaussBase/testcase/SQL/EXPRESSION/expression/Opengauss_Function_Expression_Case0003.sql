--  @testpoint:比较表达式between操作符

--a BETWEEN x  AND y等效于a >= x AND a <= y
select 1 between 0 and 2 as result;
select 1 between 3 and 4 as result;
select 'test1' between 'test0' and 'test2' as result;
select 1 between 1 and 2 as result;
select '2020-10-13' >= '2000-10-13' and '2020-10-13' <= '2050-10-13' as result;

--a NOT BETWEEN  x AND y等效于a < x OR a > y
select 1 not between 0 and 2 as result;
select 1 not between 3.5 and 6.6 as result;
select 'test1' not between 'test5.5' and 'test9.9' as result;
select 'test6.1' not between 'test5.5' and 'test9.9' as result;
select '2020-10-13' < '2000-10-13' or '2020-10-13' > '2050-10-13' as result;
select '2020-10-13' not between '2000-10-13' and '2050-10-13' as result;

--清理环境
--no need to clean