-- @testpoint: pg_size_pretty(numeric)将以数值表示的字节值转换为具有单位的易读格式。


--不指定ps可以存储任意ps的数字值，小数位会保留
     SELECT pg_size_pretty(0::numeric);
     SELECT pg_size_pretty(1024::numeric);
     SELECT pg_size_pretty(32767::numeric);
     SELECT pg_size_pretty(1024.9999::numeric);

--指定ps，只保留了整数位
    SELECT pg_size_pretty(123456.1234::NUMERIC(10,4));

--缺省的比例是 0，只保留了整数位

--s大于指定s，四舍五入,保留小数位到s
    SELECT pg_size_pretty(1024.12359::NUMERIC(20,4));

-- p-s>整数位,只保留了整数位

