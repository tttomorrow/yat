-- @testpoint: upper_inf(anyrange) 描述：上界是否为无穷

select upper_inf('(,)'::daterange) as result;
select upper_inf(int4range'(,10)') as result;
select upper_inf('(15,)'::int8range) as result;
select upper_inf(numrange(1.1,2.2)) as result;
select upper_inf(tsrange('(2021-01-01,]')) as result;
select upper_inf(tsrange('[,2021-03-01 pst]')) as result;