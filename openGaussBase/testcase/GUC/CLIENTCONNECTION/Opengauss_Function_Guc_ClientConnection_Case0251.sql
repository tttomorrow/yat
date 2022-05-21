-- @testpoint: set方法设置参数lockwait_timeout,无效值时，合理报错
--查看默认
show lockwait_timeout;
--设置，成功
set lockwait_timeout to 2147483647;
show lockwait_timeout;
--设置，报错
set lockwait_timeout to 'test';
set lockwait_timeout to '2147483647%$#';
set lockwait_timeout to '-1';
set lockwait_timeout to '2147483648';
set lockwait_timeout to 1582.256;
set lockwait_timeout to '';
--恢复默认
set lockwait_timeout to '20min';
show lockwait_timeout;