-- @testpoint: ALTER SYSTEM SET方法设置deadlock_timeout参数，合理报错
--查看默认
show deadlock_timeout;
--设置，报错
ALTER SYSTEM SET deadlock_timeout to 5;