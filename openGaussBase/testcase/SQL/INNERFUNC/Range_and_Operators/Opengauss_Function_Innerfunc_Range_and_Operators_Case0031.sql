-- @testpoint: >> 范围值是否比另一个范围值的最大值还大（没有交集）

--范围值比另一个范围值的最大值还大（没有交集），结果返回true
select int4range(5,10) >> '[1,4]'::int4range as result;
select int4range(20,25) >> '(10,20)'::int4range as result;
select int8range(25,50) >> int8range(15,25) as result;

--范围值比另一个范围值的最大值小（有交集），结果返回false
select numrange(1.1,2.2,'[]') >> numrange(5.1,6.7,'()') as result;
select tsrange('[2010-5-11 pst,2011-03-01 pst)') >> ('[2013-12-11 pst,2021-05-01 pst)') as result;
select tsrange('[1999-01-01,2000-05-01)') >> ('[2021-01-01,2021-05-01)') as result;