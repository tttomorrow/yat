-- @testpoint: 使用set方法设置除'Australia' 和 'India' 设置除此之外的时区缩写,合理报错
--查看默认值
show timezone_abbreviations;
--修改参数值为CST，报错
set timezone_abbreviations to 'CST';
--修改参数值为KOST，报错
set timezone_abbreviations to KOST;
--no need to clean