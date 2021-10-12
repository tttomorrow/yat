-- @testpoint: <@ 判断元素是否包含于函数

--元素包含于函数时，结果返回true
select  4 <@ int4range(1,5)  as result;
select 17::int8 <@ int8range(15,26)  as result;
select '2014-12-11 pst'::timestamp <@ tsrange('[2013-12-11 pst,2025-03-01 pst)') as result;
select '2026-09-09'::timestamp <@ tsrange('[2021-01-01,2028-03-01)') as result;

--元素不包含于函数时，结果返回false
select 9 <@ int4range(10,12)   as result;
select 6.1::numeric <@ numrange(8.1,10.2,'[]')  as result;