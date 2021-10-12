-- @testpoint: 函数array_lower(anyarray, int)，返回指定数组维数的下界。int为指定数组维度

--一维数组
select array_lower(array[1,2,3], 1) as result;

--三维数组
select array_lower(array[[[1,2,3], [4,5,6], [2,3,5]]], 3) as result;