-- @testpoint: ALTER SYSTEM SET方法设置lockwait_timeout参数，合理报错
-- --查看默认
show lockwait_timeout;
--设置，报错
ALTER SYSTEM SET lockwait_timeout to 600000;