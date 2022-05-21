-- @testpoint: 验证cast函数是否支持unsigned关键字,合理报错
SELECT CAST(CAST(1-2 AS UNSIGNED) AS SIGNED);
select CAST(1-2 AS UNSIGNED);