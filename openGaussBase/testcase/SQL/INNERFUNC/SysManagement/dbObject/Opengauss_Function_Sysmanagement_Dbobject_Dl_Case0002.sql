-- @testpoint: datalength(any)函数的异常校验，合理报错。

-- 不支持
   SELECT datalength('postmaster.pid');
-- 多参
    SELECT datalength(0::TINYINT，0::TINYINT);
-- 少参
    SELECT datalength();
-- 与类型不符
    SELECT datalength(256::TINYINT);
-- 数值
 -- 整数
     -- 任意精度
        -- DECIMAL[(p[,s])]
             SELECT datalength(123456.122331::DECIMAL(-10,4));
        -- NUMBER[(p[,s])]
             SELECT datalength(123456.12354::NUMERIC(10,40));

--布尔类型
    --    BOOLEAN
     SELECT datalength(yes);

--时间类型
    --    DATE
     SELECT datalength(date '13-50-2010');
