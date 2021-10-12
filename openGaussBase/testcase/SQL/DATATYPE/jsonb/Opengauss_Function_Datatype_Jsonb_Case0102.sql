-- @testpoint: Jsonb高级特性：object_json类型大小比较：使用数据库默认排序规则，正数代表大于，负数代表小于，0表示相等

-- = 相等
select '"test@dd1.."'::jsonb = '"test@dd1.."'::jsonb;
select '"123"'::jsonb = '"456"'::jsonb;
select '"12@1rr"'::jsonb = '"12#1rrf"'::jsonb;

-- <> 不相等
select '"test@dd1.."'::jsonb = '"test@dd1.."'::jsonb;
select '"123"'::jsonb = '"456"'::jsonb;
select '"12@1rr"'::jsonb = '"12#1rrf"'::jsonb;

-- > 大于
select '"test@dd1.."'::jsonb > '"test@dd1.."'::jsonb;
select '"123"'::jsonb > '"456"'::jsonb;
select '"12@1rr"'::jsonb > '"12#1rrf"'::jsonb;

-- < 小于
select '"test@dd1.."'::jsonb < '"test@dd1.."'::jsonb;
select '"123"'::jsonb < '"456"'::jsonb;
select '"12@1rr"'::jsonb < '"12#1rrf"'::jsonb;

-- >= 大于等于
select '"test@dd1.."'::jsonb >= '"test@dd1.."'::jsonb;
select '"123"'::jsonb >= '"456"'::jsonb;
select '"12@1rr"'::jsonb >= '"12#1rrf"'::jsonb;

-- <= 小于等于
select '"test@dd1.."'::jsonb <= '"test@dd1.."'::jsonb;
select '"123"'::jsonb <= '"456"'::jsonb;
select '"12@1rr"'::jsonb <= '"12#1rrf"'::jsonb;