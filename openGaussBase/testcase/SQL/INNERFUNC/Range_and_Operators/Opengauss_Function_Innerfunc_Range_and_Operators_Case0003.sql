-- @testpoint: lower(anyrange) 描述：范围的下界

select lower(int4range(10,80)) as result;
select lower(int8range(15,25)) as result;
select lower(numrange(1.1,2.2)) as result;
select lower(tsrange('[2021-01-01,2021-03-01)')) as result;
select lower(tsrange('[2013-12-11 pst,2021-03-01 pst)')) as result;

