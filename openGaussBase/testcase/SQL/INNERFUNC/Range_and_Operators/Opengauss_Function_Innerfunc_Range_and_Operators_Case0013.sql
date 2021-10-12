-- @testpoint: lower_inf(anyrange) 描述：下界是否为无穷

select lower_inf('(,)'::daterange) as result;
select lower_inf(int4range'(,10)') as result;
select lower_inf(int8range(15,25)) as result;
select lower_inf(numrange(1.1,2.2)) as result;
select lower_inf(tsrange('(2021-01-01,2021-03-01]')) as result;
select lower_inf(tsrange('[,2021-03-01 pst]')) as result;