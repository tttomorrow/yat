-- @testpoint: 使用alter system set方法设置参数TimeZone，合理报错
--查看默认值
show TimeZone;
--设置，报错
alter system set TimeZone to 'Australia/South';