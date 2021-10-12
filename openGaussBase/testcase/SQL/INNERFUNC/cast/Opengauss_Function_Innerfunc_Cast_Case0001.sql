-- @testpoint: 验证cast函数是否支持unsigned关键字,合理报错
-- @modify at: 2020-11-16
SELECT CAST(CAST(1-2 AS UNSIGNED) AS SIGNED);
select CAST(1-2 AS UNSIGNED);