-- @testpoint: 数组操作符@>，判断一个数组是否包含另一个数组

--当前面数组包含后面数组时返回true
select array[1,4,3] @> array[3,1] as result;
select array[1,3] @> array[3,1] as result;

--当前面数组不包含后面数组时返回false
select array[1,2,3] @> array[1,2,5] as result;