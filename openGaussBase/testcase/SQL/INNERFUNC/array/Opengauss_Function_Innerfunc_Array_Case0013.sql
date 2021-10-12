-- @testpoint: 函数array_prepend，向数组开头添加元素，只支持一维数组

select array_prepend(3,array[]::int[]) as result;
select array_prepend(3,array[1,2]) as result;
select array_prepend(5,array[1,2,3,2,4.1]::int[]) as result;
