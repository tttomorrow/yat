-- @testpoint: datalength(any)计算一个指定的数据需要的字节数（不考虑数据的管理空间和数据压缩，数据类型转换等情况）。

-- 数值
 -- 整数
       -- TINYINT
             SELECT datalength(0::TINYINT);
       -- SMALLINT
             SELECT datalength(-32767::SMALLINT);
       -- INTEGER
             SELECT datalength(99999::INTEGER);
       -- BINARY_INTEGER
             SELECT datalength(2147483647::BINARY_INTEGER);
       -- BIGINT
             SELECT datalength(9999999999999999::BIGINT);

     -- 任意精度
        -- DECIMAL[(p[,s])]
             SELECT datalength(123456.122331::DECIMAL(10,4));
        -- NUMBER[(p[,s])]
             SELECT datalength(123456.12354::NUMERIC(10,4));

     -- 浮点类型
        -- REAL
             SELECT datalength(10.365456::REAL);
        -- DOUBLE PRECISION
            SELECT datalength(123456.1234::DOUBLE PRECISION);
        -- BINARY_DOUBLE
            SELECT datalength(321.321::BINARY_DOUBLE);
        -- DEC[(p[,s])]
            SELECT datalength(123.123654::DECIMAL(10,4));
        -- INTEGER[(p[,s])]
           SELECT datalength(123.123654::INTEGER(6,3));


--布尔类型
    --    BOOLEAN
     SELECT datalength('n'::BOOLEAN);
     SELECT datalength('yes'::BOOLEAN);
--字符类型
    --    CHAR
     SELECT datalength('hi'::CHAR); --1
    --    CHAR(n)
     SELECT datalength('hhhh'::CHAR(5));--5
    --    CHARACTER(n)
     SELECT datalength('gyhkgkhj'::CHARACTER(6)); --6
    --    NCHAR(n)
     SELECT datalength('kkkk'::NCHAR(8));  --8
    --    VARCHAR(n)
     SELECT datalength('good'::VARCHAR(5));  --4
    --    CHARACTER
     SELECT datalength('good'::CHARACTER);  --1
    --    VARYING(n)
     SELECT datalength('good'::CHARACTER VARYING(5));  -- 4
    --    VARCHAR2(n)
     SELECT datalength('good'::VARCHAR2(8));  -- 4
    --    NVARCHAR2(n)
     SELECT datalength('good'::NVARCHAR2(9));  -- 4
    --    TEXT
     SELECT datalength('good'::TEXT); -- 4
    --    CLOB
     SELECT datalength('good'::CLOB); -- 4

--时间类型
    --    DATE
     SELECT datalength(date '12-10-2010'); --8
    --    TIME
     SELECT datalength(time '04:05:06'); --8
    --    TIMEZ
     SELECT datalength(time '04:05:06 PST'); --8
    --    TIMESTAMP
     SELECT datalength(TIMESTAMP '2010-12-12'); --8
    --    TIMESTAMPZ
     SELECT datalength('2013-12-11 pst'::TIMESTAMP);
    --    SMALLDATETIME
     SELECT datalength('2003-04-12 04:05:06'::SMALLDATETIME);  --8
    --    INTERVAL
     SELECT datalength(interval '2' year); --16
