-- @testpoint: format_type获取数据类型的SQL名称
SELECT format_type((SELECT oid FROM pg_type WHERE typname='varchar'), 10);