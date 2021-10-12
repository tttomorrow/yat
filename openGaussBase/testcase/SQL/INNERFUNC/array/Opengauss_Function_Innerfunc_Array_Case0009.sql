-- @testpoint: 数组操作符&&，判断一个数组是和另一个数组重叠（有共同元素）

--当前面数组和后面数组有重叠时时返回true
select array[1,4,3] && array[2,1] as result;

--当前面数组和后面数组无重叠时时返回true
select array[5,4,3] && array[2,1] as result;