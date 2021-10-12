-- @testpoint: 函数array_ndims，返回数组的维数

--一维数组
select array_ndims(array[4,5,6]) as result;

--二维数组
select array_ndims(array[[1,2,3], [4,5,6]]) as result;

--三维数组
select array_ndims(array[[[1,2,3], [4,5,6], [1,2,5]]]) as result;

--多维数组
select array_ndims(array[[[[[1,2,3], [4,5,6], [1,2,5]]]]]) as result;