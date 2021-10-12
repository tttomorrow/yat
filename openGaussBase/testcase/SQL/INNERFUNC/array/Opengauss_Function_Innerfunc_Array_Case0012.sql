-- @testpoint: 函数array_append，向数组末尾添加元素，合理报错

--向数组末尾添加多个元素,合理报错
select array_append(array[1,2],3,2) as result;

--向数组末尾添加非int元素,合理报错
select array_append(array[1,2],a) as result;
select array_append(array[1,2],@) as result;
select array_append(array[1,2],_) as result;

--向多维数组末尾添加单个元素,合理报错
select array_append(array[[1,2],[3,4]],2) as result;

