-- @testpoint: set方法设置参数DateStyle为无效值，合理报错
--查看默认值
show DateStyle;
--设置，报错
set DateStyle to 123;
set DateStyle to Postgres,YMD$#;
--no need to clean