-- @testpoint: set方法设置参数deadlock_timeout，无效值时，合理报错
--查看默认
show deadlock_timeout;
--设置，成功
set deadlock_timeout to 5;
show deadlock_timeout;
--设置，报错
set deadlock_timeout to 123.859;
set deadlock_timeout to 'test';
set deadlock_timeout to -1;
set deadlock_timeout to '123&^$#';
set deadlock_timeout to '';
--恢复默认
set deadlock_timeout to 1000;