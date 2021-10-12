-- @testpoint: set方法设置参数statement_timeout为无效值，合理报错
--查看默认
show statement_timeout;
--修改参数为小数，报错
set statement_timeout to 35791.156415;
--修改参数带单位s，报错
--修改参数带单位min,报错
set statement_timeout to '35792min';
--no need to clean