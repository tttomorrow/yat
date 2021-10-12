-- @testpoint: alter system set方法设置参数bytea_output值，合理报错
--查询默认
show bytea_output;
--设置，报错
alter system set bytea_output to escape;