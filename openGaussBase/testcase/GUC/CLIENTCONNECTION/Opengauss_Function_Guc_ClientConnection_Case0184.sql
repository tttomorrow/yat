-- @testpoint: ALTER SYSTEM SET方法设置update_lockwait_timeout参数，合理报错
--查看默认
show update_lockwait_timeout;
--设置，报错
ALTER SYSTEM SET update_lockwait_timeout to 600000;