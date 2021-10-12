-- @testpoint:函数之间的嵌套使用
select coalesce(exp(0),null,3);
select exp(coalesce(null,null,0,2,3));