-- @testpoint: &< 范围值的最大值是否不超过另一个范围值的最大值

--范围值的最大值不超过另一个范围值的最大值时，结果返回true
select int4range(1,5) &< '[1,4]'::int4range as result;
select int8range(15,25) &< int8range(15,25) as result;
select tsrange('[2021-01-01,2021-03-01)') &< ('[2021-01-01,2021-03-01)') as result;
select tsrange('[2013-12-11 pst,2021-03-01 pst)') &< ('[2013-12-11 pst,2021-05-01 pst)') as result;

--范围值的最大值超过另一个范围值的最大值时，结果返回false
select numrange(1.1,9.9,'[]') &< numrange(5.1,6.7,'()') as result;
select int4range(10,16) &< '(10,11)'::int4range as result;