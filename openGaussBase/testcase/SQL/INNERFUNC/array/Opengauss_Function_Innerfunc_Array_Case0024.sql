-- @testpoint: 函数array_lower(anyarray, int)，返回指定非数组维数的下界。合理报错

select array_lower([1,2,3], 1) as result;

--指定数组维度为非int类型
select array_lower(array[1,2,3], a) as result;
select array_lower(array[1,2,3], @) as result;
select array_lower(array[1,2,3], _) as result;

--指定数组维度为空
select array_lower(array[1,2,3], ) as result;