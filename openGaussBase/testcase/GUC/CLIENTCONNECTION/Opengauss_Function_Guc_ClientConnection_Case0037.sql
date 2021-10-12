-- @testpoint: set方法设置default_storage_nodegroup为新值
--查看默认值
show default_storage_nodegroup;
--设置
set default_storage_nodegroup to t_nodegroup037;
--查询
show default_storage_nodegroup;
--恢复默认
set default_storage_nodegroup to installation;
show default_storage_nodegroup;