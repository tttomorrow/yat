-- @testpoint: 函数array_cat，连接两个数组，支持多维数组

select array_cat(array[1,2,3], array[4,5]) as result;
select array_cat(array[[1,2],[4,5]], array[6,7]) as result;
select array_cat(array[[1,2],[4,5]], array[[6,7],[1,5]]) as result;