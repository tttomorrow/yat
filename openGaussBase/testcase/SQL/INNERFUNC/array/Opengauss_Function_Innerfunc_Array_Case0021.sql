-- @testpoint: 函数array_length(anyarray, int)，返回指定数组维度的长度，int为指定数组维度

select array_length(array[1,2,3],0 ) as result;
select array_length(array[1,2,3], 1) as result;
select array_length(array[[1,2,3],[4,5,6]], 2) as result;
select array_length(array[[[1,2,3,4],[4,5,6,3]]], 2) as result;
select array_length(array[[[1,2,3,4],[4,5,6,3]]], 3) as result;