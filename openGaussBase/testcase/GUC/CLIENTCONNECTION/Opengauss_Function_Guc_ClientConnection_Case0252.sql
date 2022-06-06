-- @testpoint: set方法设置参数update_lockwait_timeout,无效值时，合理报错
--查看默认
show update_lockwait_timeout;
--设置，成功
set update_lockwait_timeout to 2147483647;
show update_lockwait_timeout;
--设置，报错
set update_lockwait_timeout to 'test';
set update_lockwait_timeout to '2147483647%$#';
set update_lockwait_timeout to '-1';
set update_lockwait_timeout to '2147483648';
set update_lockwait_timeout to 1582.256;
set update_lockwait_timeout to '';
--恢复默认
set update_lockwait_timeout to 120000;
show update_lockwait_timeout;