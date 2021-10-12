-- @testpoint: 使用alter system set方法设置参数timezone_abbreviations，合理报错
--查看默认值
show timezone_abbreviations;
--设置，报错
alter system set timezone_abbreviations to 'Australia';