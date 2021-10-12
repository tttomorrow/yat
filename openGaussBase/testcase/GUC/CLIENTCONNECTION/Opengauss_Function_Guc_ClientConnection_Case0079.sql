-- @testpoint: alter system set方法设置参数值，合理报错
--查看默认
show session_replication_role;
--修改，报错
alter system set session_replication_role to local;
alter system set session_replication_role to replica;
