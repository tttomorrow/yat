-- @testpoint: @> 判断前一个函数范围是否包含后一个函数范围

--前面函数包含后面函数时，结果返回true
select int4range(1,5) @> '[1,4]'::int4range as result;
select int8range(15,26) @> int8range(15,26) as result;
select tsrange('[2013-12-11 pst,2025-03-01 pst)') @> ('[2013-12-11 pst,2021-05-01 pst)') as result;
select tsrange('[2021-01-01,2028-03-01)') @> ('[2021-01-01,2021-05-01)') as result;

--前面函数不包含后面函数时，结果返回false
select int4range(10,12) @> '(10,15)'::int4range as result;
select numrange(8.1,10.2,'[]') @> numrange(5.1,6.7,'()') as result;