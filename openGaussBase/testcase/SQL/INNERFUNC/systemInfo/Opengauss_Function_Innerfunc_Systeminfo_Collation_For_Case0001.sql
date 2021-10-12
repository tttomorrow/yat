-- @testpoint: 获取参数的排序
SELECT collation for (description) FROM pg_description LIMIT 1;
