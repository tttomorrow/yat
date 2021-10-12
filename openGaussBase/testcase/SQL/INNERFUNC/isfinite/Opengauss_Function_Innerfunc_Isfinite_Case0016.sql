-- @testpoint: isfinite有效值测试，参数为date类型
--测试判断是否为有效时间
SELECT isfinite(date '2001-02-16') from sys_dummy;
SELECT isfinite(date '2020-02-28') from sys_dummy;


