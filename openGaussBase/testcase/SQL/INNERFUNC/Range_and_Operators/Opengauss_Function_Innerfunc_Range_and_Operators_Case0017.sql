-- @testpoint: elem_contained_by_range(anyelement, anyrange) 描述：判断元素是否在范围内

select elem_contained_by_range('2', numrange(1.1,2.2));
select elem_contained_by_range('10', int4range(10,80)) as result;
select elem_contained_by_range('20', int8range(15,25)) as result;
select elem_contained_by_range('2021-02-05', tsrange('[2021-01-01,2021-03-01)')) as result;
select elem_contained_by_range('2025-12-11 pst', tsrange('[2013-12-11 pst,2021-03-01 pst)')) as result;