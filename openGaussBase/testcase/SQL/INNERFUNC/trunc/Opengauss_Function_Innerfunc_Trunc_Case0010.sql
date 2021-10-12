-- @testpoint: 数字操作函数trunc，入参为字符串测试

select trunc('856.32');
select trunc('856.32',0);
select trunc('856.32','0');
select trunc('856.323232','3');
select trunc('856.323232',3);
select trunc(856.323232,'3');