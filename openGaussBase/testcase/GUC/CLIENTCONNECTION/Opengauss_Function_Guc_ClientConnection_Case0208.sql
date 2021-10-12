-- @testpoint: set方法设置参数enable_online_ddl_waitlock，合理报错
--查看默认
show enable_online_ddl_waitlock;
--设置，报错
set enable_online_ddl_waitlock to 'on';
--no need to clean