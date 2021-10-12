-- @testpoint: jsonb格式校验：Array-jsonb（不符合格式合理报错）

--符合规范(使用反斜杠转义后，数据库显示包含反斜杠)
select '["qq",123,"null","true","false"]'::jsonb;
select '["123","null"," "]'::jsonb;
select '["123","-123","0.58","1.2345e+6"]'::jsonb;
select '[null,true,false]'::jsonb;
select '["abcdefg",123,{"db":"test"},null,"true",false]'::jsonb;
select '["abcdefg",123,{"db":789},null,"true",false]'::jsonb;
--不符合规范
select '["abcdefg",123,{"db":test}]'::jsonb;
select '[\"www@13^\", 1, {\"name\": \"john\"}, \"2\"]'::jsonb;
select '"["www@13^", 1, {"name": "john"}, "2"]"'::jsonb;