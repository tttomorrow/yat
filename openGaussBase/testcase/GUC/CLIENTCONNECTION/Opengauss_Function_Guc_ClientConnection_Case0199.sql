-- @testpoint: set方法设置参数partition_lock_upgrade_timeout,无效值时，合理报错
--查看默认
show partition_lock_upgrade_timeout;
--设置，成功
set partition_lock_upgrade_timeout to -1;
show partition_lock_upgrade_timeout;
set partition_lock_upgrade_timeout to 3000;
show partition_lock_upgrade_timeout;
--设置超临界值，报错
set partition_lock_upgrade_timeout to -2;
set partition_lock_upgrade_timeout to 3001;
--设置浮点型，报错
set partition_lock_upgrade_timeout to 1582.256;
--设置字符型，报错
set partition_lock_upgrade_timeout to 'test';
set partition_lock_upgrade_timeout to '3000%$#';
--设置空值，报错
set partition_lock_upgrade_timeout to '';
set partition_lock_upgrade_timeout to 'null';
--恢复默认
set partition_lock_upgrade_timeout to 1800;
show partition_lock_upgrade_timeout;