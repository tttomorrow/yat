-- @testpoint: power函数,参数为可以隐式转换为数值类型的字符串
select power('6.000','3.00') as result from sys_dummy;
