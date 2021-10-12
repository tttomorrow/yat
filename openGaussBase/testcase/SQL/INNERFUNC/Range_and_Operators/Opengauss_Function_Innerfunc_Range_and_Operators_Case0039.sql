-- @testpoint: - 范围函数的差集

select int4range(1,5) - '[3,4]'::int4range as result;
select int8range(16,30) -int8range(25,35) as result;
select tsrange('[2021-01-01,2021-03-01)') -('[2021-03-01,2021-10-01)') as result;
select tsrange('[2013-12-11 pst,2021-03-01 pst)') -('[2021-3-01 pst,2021-05-01 pst)') as result;
select tsrange('[2021-01-01,2021-03-01)') - ('[2021-3-01 pst,2021-05-01 pst)') as result;
select int4range(10,16) - '(10,11)'::int4range as result;
select int8range(16,25) -int8range(15,35) as result;