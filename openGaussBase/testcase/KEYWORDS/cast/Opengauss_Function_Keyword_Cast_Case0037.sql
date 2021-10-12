--  @testpoint:验证cast函数是否支持unsigned关键字
select cast(cast(1-2 as unsigned) as signed);
