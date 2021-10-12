-- @testpoint: jsonb格式校验：Str-jsonb（不符合格式合理报错）

--符合规范(使用反斜杠转义后，数据库显示包含反斜杠)
select '"abcdefg"'::jsonb;
select '"1"'::jsonb;
select '"$$"'::jsonb;
select '"\"$$\""'::jsonb;
select '"[\"www@13^\", 1, {\"name\": \"john\"}, \"2\"]"'::jsonb;

--不符合规范
select 'abcdefg'::jsonb;
select '''abcdefg'''::jsonb;
select '\"$$\"'::jsonb;
select '"["www@13^", 1, {"name": "john"}, "2"]"'::jsonb;