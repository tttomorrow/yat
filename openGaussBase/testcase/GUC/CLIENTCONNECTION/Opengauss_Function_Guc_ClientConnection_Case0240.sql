-- @testpoint: 使用ALTER SYSTEM SET 方法设置参数dynamic_library_path，合理报错
ALTER SYSTEM SET dynamic_library_path = '/home';
--no need to clean