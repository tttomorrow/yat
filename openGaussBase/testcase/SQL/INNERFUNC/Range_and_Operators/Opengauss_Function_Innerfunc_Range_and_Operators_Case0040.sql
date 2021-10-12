-- @testpoint: - 范围函数的差集，当范围函数类型不同时，合理报错

select int4range(1,3) - int8range(25,35) as result;
select tsrange('[2021-01-01,2021-03-01)') - '[3,4]'::int4range  as result;