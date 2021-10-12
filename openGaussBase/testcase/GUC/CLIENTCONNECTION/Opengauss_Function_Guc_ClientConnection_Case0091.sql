-- @testpoint: alter system set方法设置参数vacuum_freeze_min_age值，合理报错
--查询默认
show vacuum_freeze_min_age;
--设置，报错
alter system set vacuum_freeze_min_age to 52002333;
--no need to clean