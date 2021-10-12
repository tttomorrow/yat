-- @testpoint: upper_inc(anyrange) 描述：是否包含上界

select upper_inc(int4range(10,10)) as result;
select upper_inc(int8range(15,25)) as result;
select upper_inc(numrange(1.1,2.2)) as result;
select upper_inc(tsrange('(2021-01-01,2021-03-01]')) as result;
select upper_inc(tsrange('[2013-12-11 pst,2021-03-01 pst]')) as result;