-- @testpoint: isfinite有效值测试，参数为interval类型
--测试是否为有效区间
SELECT isfinite(interval '4 hours') from sys_dummy;
SELECT isfinite(interval '0 hours') from sys_dummy;