-- @testpoint: 使用alter system set方法设置参数check_function_bodies为off，合理报错
--查看默认
show check_function_bodies;
--修改，报错
ALTER SYSTEM SET check_function_bodies to off;