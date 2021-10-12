-- @testpoint: 函数unnest(anyarray)，描述：扩大一个数组为一组行

select unnest(array[1,2]) as result;
select unnest(array[1,2,3,4,5]) as result;