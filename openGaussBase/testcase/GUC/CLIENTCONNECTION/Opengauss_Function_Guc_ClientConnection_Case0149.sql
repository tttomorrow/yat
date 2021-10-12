-- @testpoint: ALTER SYSTEM SET方法设置lc_monetary参数，合理报错
--查询默认
show lc_monetary;
--设置，报错
ALTER SYSTEM SET lc_monetary to 'C';
--no need to clean