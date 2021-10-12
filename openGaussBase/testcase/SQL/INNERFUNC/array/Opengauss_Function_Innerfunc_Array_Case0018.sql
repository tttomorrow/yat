-- @testpoint: 函数array_ndims，返回数组的维数，非数组时合理报错

select array_ndims(array[1,2,a]) as result;
select array_ndims(array[[1,2,a],[2,3,5]]) as result;