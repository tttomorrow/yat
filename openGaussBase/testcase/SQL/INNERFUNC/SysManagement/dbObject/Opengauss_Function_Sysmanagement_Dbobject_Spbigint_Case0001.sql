-- @testpoint: pg_size_pretty(bigint)将以64位整数表示的字节值转换为具有单位的易读格式。


-- BIGINT
     SELECT pg_size_pretty(0::BIGINT);
     SELECT pg_size_pretty(1024::BIGINT);
     SELECT pg_size_pretty(32767::BIGINT);
