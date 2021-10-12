-- @testpoint: json格式校验：Str-json（不符合格式合理报错）

--符合规范(使用反斜杠转义后，数据库显示包含反斜杠)
select '"abcdefg"'::json;
select '"1"'::json;
select '"$$"'::json;
select '"\"$$\""'::json;
select '"[\"www@13^\", 1, {\"name\": \"john\"}, \"2\"]"'::json;

--不符合规范
select 'abcdefg'::json;
select '''abcdefg'''::json;
select '\"$$\"'::json;
select '"["www@13^", 1, {"name": "john"}, "2"]"'::json;