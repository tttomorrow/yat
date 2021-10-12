-- @testpoint: set方法设置参数local_preload_libraries，合理报错
--查看默认
show local_preload_libraries;
--set方法设置，报错
SET local_preload_libraries to '/home';
--no need to clean