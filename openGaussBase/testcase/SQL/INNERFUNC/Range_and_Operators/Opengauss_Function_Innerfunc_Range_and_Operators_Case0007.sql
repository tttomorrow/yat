-- @testpoint: isempty(anyrange) 描述：范围是否为空

select isempty(int4range(10,10)) as result;
select isempty(int8range(15,25)) as result;
select isempty(numrange(1.1,2.2)) as result;
select isempty(tsrange('[2021-01-01,2021-03-01)')) as result;
select isempty(tsrange('[2013-12-11 pst,2021-03-01 pst)')) as result;