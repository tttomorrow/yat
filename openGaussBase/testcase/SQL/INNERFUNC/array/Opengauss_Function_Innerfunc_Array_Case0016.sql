-- @testpoint: 函数array_cat，连接两个数组，合理报错

--连接两个数组维度不一样的多维数组，合理报错
select array_cat(array[[1,2,3],[2,5]], array[[4,5],[1,2]]) as result;

--连接数组和元素，合理报错
select array_cat(array[[1,2,3],[2,5]], 5) as result;

--连接数组和非int元素，合理报错
select array_cat(array[[1,2,3],[2,5]], a) as result;
select array_cat(array[[1,2,3],[2,5]], @) as result;
select array_cat(array[[1,2,3],[2,5]], _) as result;