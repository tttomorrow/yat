-- @testpoint: set方法设置参数fault_mon_timeout，合理报错
--查看默认
show fault_mon_timeout;
--设置，报错
set fault_mon_timeout to 10;
--no need to clean