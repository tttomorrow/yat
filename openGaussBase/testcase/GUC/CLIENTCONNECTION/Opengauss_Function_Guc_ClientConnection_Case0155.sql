-- @testpoint: ALTER SYSTEM SET方法设置lc_numeric参数，合理报错
--查询默认
show lc_numeric;
--设置，报错
ALTER SYSTEM SET lc_numeric to 'C';
--no need to clean
