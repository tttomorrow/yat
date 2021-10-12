-- @testpoint: 函数array_to_string(anyarray, text [, text])，描述使用第一个text作为数组的新分隔符，使用第二个text替换数组值为null的值。

--数组中有null
select array_to_string(array[1, 2, 3, null, 5], ',', '*') as result;
select array_to_string(array[1, 2, 3, null, 5], '_', '6') as result;
select array_to_string(array[1, 2, 3, null, 5], '8', '6') as result;

--数组中没有null
select array_to_string(array[1, 2, 3, 5], ',', '*') as result;