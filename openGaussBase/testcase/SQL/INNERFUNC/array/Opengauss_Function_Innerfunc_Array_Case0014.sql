-- @testpoint: 函数array_prepend，向数组开头添加元素，合理报错

--向数组开头添加多个元素,合理报错
select array_prepend(3,2,array[1,2]) as result;

--向数组开头添加非int元素,合理报错
select array_prepend(a,array[1,2]) as result;
select array_prepend(@,array[1,2]) as result;
select array_prepend(_,array[1,2]) as result;

--向多维数组开头添加单个元素,合理报错
select array_prepend(2,array[[1,2],[3,4]]) as result;
