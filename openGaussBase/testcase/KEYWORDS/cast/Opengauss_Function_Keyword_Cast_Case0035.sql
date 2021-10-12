-- @testpoint: cast函数中是否支持now()函数嵌套，合理报错

 select cast(now() as int) from sys_dummy;