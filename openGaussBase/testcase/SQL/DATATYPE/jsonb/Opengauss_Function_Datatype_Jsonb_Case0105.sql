-- @testpoint: Jsonb高级特性：array-jsonb类型：1.长度长的 > 长度短的 2.长度相同则依次比较数组里的每个元素

-- = 相等:长度不同
select '["","","","a"]'::jsonb = '["a"]'::jsonb;
select '["",""]'::jsonb = '[""]'::jsonb;
select '["123", 123, "@123"]'::jsonb = '["wsd", 567]'::jsonb;
-- = 相等:长度相同
select '["yyy", 1, "2er"]'::jsonb = '["zzz", 1, "2er"]'::jsonb;
select '[1,"er", false]'::jsonb = '[1,"er", true]'::jsonb;
select '["abc"]'::jsonb = '["bcd"]'::jsonb;
select '[null]'::jsonb = '[""]'::jsonb;
select '[1,"er", {"a":1, "b":2}]'::jsonb = '[1,"er", {"a":2, "b":2}]'::jsonb;
select '["1?N", "0"]'::jsonb = '["2M?", "0"]'::jsonb;
select '["zyx"]'::jsonb = '["?Mld"]'::jsonb;

-- <> 不相等:长度不同
select '["","","","a"]'::jsonb <> '["a"]'::jsonb;
select '["",""]'::jsonb <> '[""]'::jsonb;
select '["123", 123, "@123"]'::jsonb <> '["wsd", 567]'::jsonb;
-- <> 不相等:长度相同
select '["yyy", 1, "2er"]'::jsonb <> '["zzz", 1, "2er"]'::jsonb;
select '[1,"er", false]'::jsonb <> '[1,"er", true]'::jsonb;
select '["abc"]'::jsonb <> '["bcd"]'::jsonb;
select '[null]'::jsonb <>'[""]'::jsonb;
select '[1,"er", {"a":1, "b":2}]'::jsonb <> '[1,"er", {"a":2, "b":2}]'::jsonb;

-- > 大于:长度不同
select '["","","","a"]'::jsonb > '["a"]'::jsonb;
select '["",""]'::jsonb > '[""]'::jsonb;
select '["123", 123, "@123"]'::jsonb > '["wsd", 567]'::jsonb;
-- > 大于:长度相同
select '["yyy", 1, "2er"]'::jsonb > '["zzz", 1, "2er"]'::jsonb;
select '[1,"er", false]'::jsonb > '[1,"er", true]'::jsonb;
select '["abc"]'::jsonb > '["bcd"]'::jsonb;
select '[null]'::jsonb >'[""]'::jsonb;
select '[1,"er", {"a":1, "b":2}]'::jsonb > '[1,"er", {"a":2, "b":2}]'::jsonb;

-- < 小于:长度不同
select '["","","","a"]'::jsonb < '["a"]'::jsonb;
select '["",""]'::jsonb < '[""]'::jsonb;
select '["123", 123, "@123"]'::jsonb < '["wsd", 567]'::jsonb;
-- < 小于:长度相同
select '["yyy", 1, "2er"]'::jsonb < '["zzz", 1, "2er"]'::jsonb;
select '[1,"er", false]'::jsonb < '[1,"er", true]'::jsonb;
select '["abc"]'::jsonb < '["bcd"]'::jsonb;
select '[null]'::jsonb < '[""]'::jsonb;
select '[1,"er", {"a":1, "b":2}]'::jsonb < '[1,"er", {"a":2, "b":2}]'::jsonb;

-- >= 大于等于:长度不同
select '["","","","a"]'::jsonb >= '["a"]'::jsonb;
select '["",""]'::jsonb >= '[""]'::jsonb;
select '["123", 123, "@123"]'::jsonb >= '["wsd", 567]'::jsonb;
-- >= 大于等于:长度相同
select '["yyy", 1, "2er"]'::jsonb >= '["zzz", 1, "2er"]'::jsonb;
select '[1,"er", false]'::jsonb >= '[1,"er", true]'::jsonb;
select '["abc"]'::jsonb >= '["bcd"]'::jsonb;
select '[null]'::jsonb >= '[""]'::jsonb;
select '[1,"er", {"a":1, "b":2}]'::jsonb >= '[1,"er", {"a":2, "b":2}]'::jsonb;

-- <= 小于等于:长度不同
select '["","","","a"]'::jsonb <= '["a"]'::jsonb;
select '["",""]'::jsonb <= '[""]'::jsonb;
select '["123", 123, "@123"]'::jsonb <= '["wsd", 567]'::jsonb;
-- <= 小于等于:长度相同
select '["yyy", 1, "2er"]'::jsonb <= '["zzz", 1, "2er"]'::jsonb;
select '[1,"er", false]'::jsonb <= '[1,"er", true]'::jsonb;
select '["abc"]'::jsonb <= '["bcd"]'::jsonb;
select '[null]'::jsonb <= '[""]'::jsonb;
select '[1,"er", {"a":1, "b":2}]'::jsonb <= '[1,"er", {"a":2, "b":2}]'::jsonb;