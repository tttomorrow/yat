-- @testpoint: 使用set方法设置max_compile_functions参数值，合理报错
--查看默认
show max_compile_functions;
--设置，报错
set max_compile_functions to 1;