-- @testpoint: elem_contained_by_range(anyelement, anyrange),判断元素是否在范围内,入参为无效值时，合理报错

select elem_contained_by_range('abc', int8range(15,25)) as result;
select elem_contained_by_range(2, numrange(1.1,2.2)) as result;