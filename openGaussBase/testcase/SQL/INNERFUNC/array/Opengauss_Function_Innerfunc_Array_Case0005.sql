-- @testpoint: 数组操作符<=，判断一个数组是否小于或等于另一个数组

--当前面数组小于等于后面数组时返回true
select array[1,2,3] <= array[1,2,3] as result;
select array[1,2,3] <= array[1,2,4] as result;

--当前面数组不小于等于后面数组时返回false
select array[1,4,3] <= array[1,2,3] as result;
