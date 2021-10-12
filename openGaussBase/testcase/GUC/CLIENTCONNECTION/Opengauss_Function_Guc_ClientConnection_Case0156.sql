-- @testpoint: ALTER SYSTEM SET方法设置lc_time参数，合理报错
--查询默认
show lc_time;
--设置，报错
ALTER SYSTEM SET lc_time to 'C';
--no need to clean