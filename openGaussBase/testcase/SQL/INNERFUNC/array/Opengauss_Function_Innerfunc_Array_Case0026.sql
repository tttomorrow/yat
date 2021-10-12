-- @testpoint: 函数array_upper(anyarray, int)描述：返回指定数组维数的上界。指定数组维度为非int,合理报错
select array_upper(array[1,8,3,7], a) as result;
select array_upper(array[1,8,3,7], _) as result;
select array_upper(array[[1,8,3,7]], #) as result;
select array_upper(array[[1,8,3,7]], ) as result;