-- @testpoint: pg_size_pretty(numeric)函数的异常校验，合理报错



--numeric(p [,s])，p:[1,1000], [s>=0]

    --整数位 >p-s，溢出
    SELECT pg_size_pretty(123456789.1234::NUMERIC(10,4));
    -- p>1000、p为负
    SELECT pg_size_pretty(1024::numeric(1001));
    SELECT pg_size_pretty(1024::numeric(-9));
    -- s为负
    SELECT pg_size_pretty(123456.1234::NUMERIC(10,-4));
    -- 不是数值类型
    SELECT pg_size_pretty('abcd');
    SELECT pg_size_pretty(0x5f);