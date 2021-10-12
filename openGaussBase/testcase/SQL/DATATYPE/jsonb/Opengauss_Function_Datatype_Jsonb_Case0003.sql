-- @testpoint: openGauss可否正确判断JSON类型:字符串（不符合规范的合理报错）

--符合规范(使用反斜杠转义后，数据库显示包含反斜杠)
select '"abcdefg"'::JSON;
select '"1"'::JSON;
select '"$$"'::JSON;
select '"\"$$\""'::JSON;
select '"[\"www@13^\", 1, {\"name\": \"john\"}, \"2\"]"'::JSON;

--不符合规范
select 'abcdefg'::JSON;
select '''abcdefg'''::JSON;
select '\"$$\"'::JSON;
select '"["www@13^", 1, {"name": "john"}, "2"]"'::JSON;