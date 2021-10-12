-- @testpoint: 使用alter system set方法设置参数DateStyle，合理报错
--查看默认值
show DateStyle;
--设置，报错
alter system set DateStyle to YMD;