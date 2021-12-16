-- @testpoint: pg_column_size(any)存储一个指定的数值需要的字节数（可能压缩过）

-- 未压缩
 -- 整数
   -- TINYINT
         SELECT pg_column_size(0::TINYINT);
         SELECT pg_column_size(8::TINYINT);
         SELECT pg_column_size(255::TINYINT);
   -- SMALLINT
         SELECT pg_column_size(-32767::SMALLINT);
         SELECT pg_column_size(-8::SMALLINT);
         SELECT pg_column_size(0::SMALLINT);
         SELECT pg_column_size(9::SMALLINT);
         SELECT pg_column_size(32767::SMALLINT);
   -- INTEGER
         SELECT pg_column_size(-2147483647::INTEGER);
         SELECT pg_column_size(-88888::INTEGER);
         SELECT pg_column_size(0::INTEGER);
         SELECT pg_column_size(99999::INTEGER);
         SELECT pg_column_size(2147483647::INTEGER);
   -- BINARY_INTEGER
         SELECT pg_column_size(-2147483647::BINARY_INTEGER);
         SELECT pg_column_size(-8::BINARY_INTEGER);
         SELECT pg_column_size(0::BINARY_INTEGER);
         SELECT pg_column_size(9::BINARY_INTEGER);
         SELECT pg_column_size(2147483647::BINARY_INTEGER);
   -- BIGINT
         SELECT pg_column_size(-9223372036854775807::BIGINT);
         SELECT pg_column_size(-888888888888888::BIGINT);
         SELECT pg_column_size(0::BIGINT);
         SELECT pg_column_size(9999999999999999::BIGINT);
         SELECT pg_column_size(9223372036854775807::BIGINT);
 -- 任意精度
    -- DECIMAL[(p[,s])]
         SELECT pg_column_size(123456.122331::DECIMAL(10,4));
    -- NUMBER[(p[,s])]
         SELECT pg_column_size(123456.12354::NUMERIC(10,4));

 -- 浮点类型
    -- REAL
         SELECT pg_column_size(10.365456::REAL);
    -- DOUBLE PRECISION
        SELECT pg_column_size(123456.1234::DOUBLE PRECISION);
    -- BINARY_DOUBLE
        SELECT pg_column_size(321.321::BINARY_DOUBLE);
    -- DEC[(p[,s])]
        SELECT pg_column_size(123.123654::DECIMAL(10,4));
    -- INTEGER[(p[,s])]
       SELECT pg_column_size(123.123654::INTEGER(6,3));

-- 压缩过的数值：压缩存在列存表当中
     CREATE TABLE table1
        (
          num    integer,
          date1  character(100)
        ) WITH (ORIENTATION = COLUMN);
     INSERT INTO table1 VALUES (9999, '20200910');
     SELECT pg_column_size(num) from table1  limit 1;
     DROP TABLE table1;