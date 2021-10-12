-- @testpoint: json格式校验：Array-json（不符合格式合理报错）

--符合规范
select '["qq",123,"null","true","false"]'::json;
select '["123","null"," "]'::json;
select '["123","-123","0.58","1.2345e+6"]'::json;
select '[null,true,false]'::json;
select '["abcdefg",123,{"db":"test"},null,"true",false]'::json;
select '["abcdefg",123,{"db":789},null,"true",false]'::json;
--不符合规范
select '["abcdefg",123,{"db":test}]'::json;
select '[\"www@13^\", 1, {\"name\": \"john\"}, \"2\"]'::json;
select '"["www@13^", 1, {"name": "john"}, "2"]"'::json;