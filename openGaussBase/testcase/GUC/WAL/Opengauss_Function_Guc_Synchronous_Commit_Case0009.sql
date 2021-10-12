-- @testpoint: 使用ALTER SYSTEM SET 方法设置参数synchronous_commit值为2，合理报错
--使用ALTER SYSTEM SET 方法设置参数值;ERROR:  unsupport parameter: synchronous_commit
alter system set synchronous_commit to 2;
--no need to clean
