-- @testpoint: 获取任何值的数据类型
SELECT pg_typeof(33);
SELECT typlen FROM pg_type WHERE oid = pg_typeof(33);