-- @testpoint: pg_column_size(any)函数的异常校验，合理报错

-- 未压缩
 -- 整数
   -- TINYINT
         SELECT pg_column_size(-90::TINYINT);
         SELECT pg_column_size('0x89'::TINYINT);
         SELECT pg_column_size(256::TINYINT);
         SELECT pg_column_size(255::TINYINT,255::TINYINT);
   -- SMALLINT
         SELECT pg_column_size(-32768::SMALLINT);
         SELECT pg_column_size('*&&^&'9::SMALLINT);
         SELECT pg_column_size(32768::SMALLINT);
   -- INTEGER
         SELECT pg_column_size(-2147483648::INTEGER);
         SELECT pg_column_size('hijk'::clob);
         SELECT pg_column_size(2147483648::INTEGER);
   -- BINARY_INTEGER
         SELECT pg_column_size(-2147483648::BINARY_INTEGER);
         SELECT pg_column_size(高斯);
         SELECT pg_column_size(2147483648::BINARY_INTEGER);
   -- BIGINT
         SELECT pg_column_size();
         SELECT pg_column_size(‘’);
         SELECT pg_column_size('');
