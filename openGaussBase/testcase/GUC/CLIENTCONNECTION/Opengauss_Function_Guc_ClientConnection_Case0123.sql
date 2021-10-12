-- @testpoint: 使用alter system set方法设置参数gin_pending_list_limit，合理报错
--查看默认值
show gin_pending_list_limit;
--设置，报错
alter system set gin_pending_list_limit to 64;