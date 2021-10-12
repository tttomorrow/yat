-- @testpoint: Jsonb高级特性：num-jsonb类型大小比较：数值比较

-- = 相等
select '123.0'::jsonb = '123'::jsonb;
select '1235e-5'::jsonb = '1.235e-2'::jsonb;
select '-789'::jsonb = '123'::jsonb;
select '110'::jsonb = '-119'::jsonb;

-- <> 不相等
select '123.0'::jsonb <> '123'::jsonb;
select '1235e-5'::jsonb <> '1.235e-2'::jsonb;
select '-789'::jsonb <> '123'::jsonb;
select '110'::jsonb <> '-119'::jsonb;

-- > 大于
select '123.0'::jsonb > '123'::jsonb;
select '1235e-5'::jsonb > '1.235e-2'::jsonb;
select '-789'::jsonb > '123'::jsonb;
select '110'::jsonb  > '-119'::jsonb;

-- < 小于
select '123.0'::jsonb < '123'::jsonb;
select '1235e-5'::jsonb < '1.235e-2'::jsonb;
select '-789'::jsonb < '123'::jsonb;
select '110'::jsonb < '-119'::jsonb;

-- >= 大于等于
select '123.0'::jsonb >= '123'::jsonb;
select '1235e-5'::jsonb >= '1.235e-2'::jsonb;
select '-789'::jsonb >= '123'::jsonb;
select '110'::jsonb >= '-119'::jsonb;

-- <= 小于等于
select '123.0'::jsonb <= '123'::jsonb;
select '1235e-5'::jsonb <= '1.235e-2'::jsonb;
select '-789'::jsonb <= '123'::jsonb;
select '110'::jsonb <= '-119'::jsonb;
