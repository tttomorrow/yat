-- @testpoint: 参数default_statistics_target测试,无效取值，合理报错
--查看默认值（100）
show default_statistics_target;
--使用set方式设置参数值
set default_statistics_target = -100;
--查看参数值（-100）
show default_statistics_target;
--使用set方式设置参数值
set default_statistics_target = 10000;
--查看参数值（10000）
show default_statistics_target;
--使用set方式设置参数为无效值，合理报错，ERROR:  -101 is outside the valid range for parameter "default_statistics_target" (-100 .. 10000)
set default_statistics_target = -101;
set default_statistics_target = 10001;
--设置参数值包含特殊字符，ERROR:  invalid value for parameter "default_statistics_target": "100*&^%"
set default_statistics_target = '100*&^%';
--设置参数值为小数，ERROR:  invalid value for parameter "default_statistics_target": "100.558"
set default_statistics_target = 100.558;
--恢复设置
reset default_statistics_target;