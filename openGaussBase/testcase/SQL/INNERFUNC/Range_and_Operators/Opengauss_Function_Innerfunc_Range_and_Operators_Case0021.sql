-- @testpoint: <, 判断前面函数是否小于后面函数

--前面函数小于后面函数时，结果返回true
select numrange(1.1,2.2,'[]') < numrange(5.1,6.7,'()') as result;
select tsrange('[2013-12-11 pst,2021-03-01 pst)') < ('[2013-12-11 pst,2021-05-01 pst)') as result;
select tsrange('[2021-01-01,2021-03-01)') < ('[2021-01-01,2021-05-01)') as result;

--前面函数不小于后面函数时，结果返回false
select int4range(1,5) < '[1,4]'::int4range as result;
select int4range(10,10) < '(10,11)'::int4range as result;
select int8range(15,25) < int8range(15,25) as result;
