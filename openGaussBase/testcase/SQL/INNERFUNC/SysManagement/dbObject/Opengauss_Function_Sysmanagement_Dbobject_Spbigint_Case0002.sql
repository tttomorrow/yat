-- @testpoint: pg_size_pretty(bigint)函数的异常校验，合理报错

-- 负数、其它数值类型、多参、少参、空值、边界值外
-- BIGINT

     SELECT pg_size_pretty(1024::BIGINT,1024::BIGINT);
     SELECT pg_size_pretty();
     SELECT pg_size_pretty('hik');

     SELECT pg_size_pretty(32768::SMALLINT);
     SELECT pg_size_pretty('');