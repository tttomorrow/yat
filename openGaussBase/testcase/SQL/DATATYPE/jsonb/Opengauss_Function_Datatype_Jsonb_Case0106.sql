-- @testpoint: Jsonb高级特性：object-jsonb类型:1.长度长的 > 长度短的2.长度相同则依次比较数组里的每个键值对，先比较键，再比较值

-- = 相等:长度不同
select '{"a":1, "b":"test", "a":2}'::jsonb = '{"a":2, "b":"test"}'::jsonb;
select '{"a":1,"b":2,"c":3}'::jsonb = '{"d":1,"b":2}'::jsonb;
-- = 相等:长度相同
select '{"test": "...", "dbf": false}'::jsonb = '{"dbf": false, "test": "..."  }'::jsonb;
select '{"a":1, "b":2}'::jsonb = '{"a":1, "b":false}'::jsonb;
select '{"a":[1,2,3], "b":null}'::jsonb = '{"a":[1,2,3,4], "b":true}'::jsonb;
select '{"a":1, "b":false}'::jsonb = '{"a":1, "b":false}'::jsonb;

-- <> 不相等:长度不同
select '{"a":1, "b":"test", "a":2}'::jsonb <> '{"a":2, "b":"test"}'::jsonb;
select '{"a":1,"b":2,"c":3}'::jsonb <> '{"d":1,"b":2}'::jsonb;
-- <> 不相等:长度相同
select '{"test": "...", "dbf": false}'::jsonb <> '{"dbf": false, "test": "..."  }'::jsonb;
select '{"a":1, "b":2}'::jsonb <> '{"a":1, "b":false}'::jsonb;
select '{"a":[1,2,3], "b":null}'::jsonb <> '{"a":[1,2,3,4], "b":true}'::jsonb;
select '{"a":1, "b":false}'::jsonb <> '{"a":1, "b":false}'::jsonb;

-- > 大于:长度不同
select '{"a":1, "b":"test", "a":2}'::jsonb > '{"a":2, "b":"test"}'::jsonb;
select '{"a":1,"b":2,"c":3}'::jsonb > '{"d":1,"b":2}'::jsonb;
-- > 大于:长度相同
select '{"test": "...", "dbf": false}'::jsonb > '{"dbf": false, "test": "..."  }'::jsonb;
select '{"a":1, "b":2}'::jsonb > '{"a":1, "b":false}'::jsonb;
select '{"a":[1,2,3], "b":null}'::jsonb > '{"a":[1,2,3,4], "b":true}'::jsonb;
select '{"a":1, "b":false}'::jsonb > '{"a":1, "b":false}'::jsonb;

-- < 小于:长度不同
select '{"a":1, "b":"test", "a":2}'::jsonb < '{"a":2, "b":"test"}'::jsonb;
select '{"a":1,"b":2,"c":3}'::jsonb < '{"d":1,"b":2}'::jsonb;
-- < 小于:长度相同
select '{"test": "...", "dbf": false}'::jsonb < '{"dbf": false, "test": "..."  }'::jsonb;
select '{"a":1, "b":2}'::jsonb < '{"a":1, "b":false}'::jsonb;
select '{"a":[1,2,3], "b":null}'::jsonb < '{"a":[1,2,3,4], "b":true}'::jsonb;
select '{"a":1, "b":false}'::jsonb < '{"a":1, "b":false}'::jsonb;

-- >= 大于等于:长度不同
select '{"a":1, "b":"test", "a":2}'::jsonb >= '{"a":2, "b":"test"}'::jsonb;
select '{"a":1,"b":2,"c":3}'::jsonb >= '{"d":1,"b":2}'::jsonb;
-- >= 大于等于:长度相同
select '{"test": "...", "dbf": false}'::jsonb >= '{"dbf": false, "test": "..."  }'::jsonb;
select '{"a":1, "b":2}'::jsonb >= '{"a":1, "b":false}'::jsonb;
select '{"a":[1,2,3], "b":null}'::jsonb >= '{"a":[1,2,3,4], "b":true}'::jsonb;
select '{"a":1, "b":false}'::jsonb >= '{"a":1, "b":false}'::jsonb;

-- <= 小于等于:长度不同
select '{"a":1, "b":"test", "a":2}'::jsonb <= '{"a":2, "b":"test"}'::jsonb;
select '{"a":1,"b":2,"c":3}'::jsonb <= '{"d":1,"b":2}'::jsonb;
-- <= 小于等于:长度相同
select '{"test": "...", "dbf": false}'::jsonb <= '{"dbf": false, "test": "..."  }'::jsonb;
select '{"a":1, "b":2}'::jsonb <= '{"a":1, "b":false}'::jsonb;
select '{"a":[1,2,3], "b":null}'::jsonb <= '{"a":[1,2,3,4], "b":true}'::jsonb;
select '{"a":1, "b":false}'::jsonb <= '{"a":1, "b":false}'::jsonb;