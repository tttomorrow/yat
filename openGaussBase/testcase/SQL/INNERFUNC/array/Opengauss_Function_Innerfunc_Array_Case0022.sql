-- @testpoint: 函数array_length(anyarray, int)，返回指定数组维度的长度，指定数组维度非int类型，合理报错

--指定数组维度为空
select array_length(array[1,2,3], ) as result;

--指定数组维度为非int类型
select array_length(array[1,2,3],a) as result;
select array_length(array[1,2,3],_) as result;