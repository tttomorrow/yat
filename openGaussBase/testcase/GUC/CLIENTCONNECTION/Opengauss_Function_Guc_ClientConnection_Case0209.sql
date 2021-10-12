-- @testpoint: alter system set方法设置参数enable_online_ddl_waitlock为无效值，合理报错
--查看默认
show enable_online_ddl_waitlock;
--设置,报错
ALTER SYSTEM SET enable_online_ddl_waitlock to 1234;
ALTER SYSTEM SET enable_online_ddl_waitlock to 'abc';
ALTER SYSTEM SET enable_online_ddl_waitlock to 'on%$#';
--设置空串，报错
ALTER SYSTEM SET enable_online_ddl_waitlock to '';
ALTER SYSTEM SET enable_online_ddl_waitlock to 'null';
--no need to clean