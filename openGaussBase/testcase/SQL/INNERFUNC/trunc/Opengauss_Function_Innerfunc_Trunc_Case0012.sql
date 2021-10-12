-- @testpoint: 数字操作函数trunc，入参中嵌套函数

select trunc(trunc(456.23,1),2);
select trunc(trunc(456.23,'1'),2);
select trunc(trunc(456.23,'1'),'2');