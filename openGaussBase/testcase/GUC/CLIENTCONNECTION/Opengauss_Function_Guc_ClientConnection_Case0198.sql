-- @testpoint: ALTER SYSTEM SET方法设置partition_lock_upgrade_timeout参数，合理报错
--查看默认
show partition_lock_upgrade_timeout;
--设置，报错
ALTER SYSTEM SET partition_lock_upgrade_timeout to 2000;
--no need to clean