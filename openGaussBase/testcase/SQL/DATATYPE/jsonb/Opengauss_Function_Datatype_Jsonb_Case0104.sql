-- @testpoint: Jsonb高级特性：bool-jsonb类型：true > false

-- = 相等
select 'true'::jsonb = 'true'::jsonb;
select 'false'::jsonb = 'true'::jsonb;
select 'false'::jsonb = 'false'::jsonb;

-- <> 不相等
select 'true'::jsonb <> 'true'::jsonb;
select 'false'::jsonb <> 'true'::jsonb;
select 'false'::jsonb <> 'false'::jsonb;

-- > 大于
select 'true'::jsonb > 'true'::jsonb;
select 'false'::jsonb > 'true'::jsonb;
select 'false'::jsonb > 'false'::jsonb;

-- < 小于
select 'true'::jsonb < 'true'::jsonb;
select 'false'::jsonb < 'true'::jsonb;
select 'false'::jsonb < 'false'::jsonb;

-- >= 大于等于
select 'true'::jsonb >= 'true'::jsonb;
select 'false'::jsonb >= 'true'::jsonb;
select 'false'::jsonb >= 'false'::jsonb;

-- <= 小于等于
select 'true'::jsonb <= 'true'::jsonb;
select 'false'::jsonb <= 'true'::jsonb;
select 'false'::jsonb <= 'false'::jsonb;

