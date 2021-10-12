-- @testpoint: 通用函数：jsonb_extract_path_text_op（在指定的路径获取JSON对象为text,等效于#>>操作符，当入参不合理时，合理报错）

--jsonb_extract_path_text_op函数，入参合理
select jsonb_extract_path_text_op('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}','{"f4","f6"}');
select jsonb_extract_path_text_op ('{"f1":[1,2,3],"f2":{"f3":1},"f4":null}','{"f2","f3"}');
select jsonb_extract_path_text_op ('{"a":1, "b":"test", "a":2,"b":true}','{"a",4}');
select jsonb_extract_path_text_op ('{"a": {"b":{"a":{"b":{"a":{"b":88}}}}}}','{"a","b"}');
select jsonb_extract_path_text_op ('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]','{"a",4}');
select jsonb_extract_path_text_op ('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]','{2}');

--jsonb_extract_path_text_op函数，入参不合理
select jsonb_extract_path_text_op ('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]',{2});
select jsonb_extract_path_text_op('true','true');
select jsonb_extract_path_text_op('1389158','138');
select jsonb_extract_path_text_op('null','n');
select jsonb_extract_path_text_op('true,false','true');
select jsonb_extract_path_text_op('138,158,369','138');
select jsonb_extract_path_text_op('null',‘{1)’;

--返回结果类型校验：text
select pg_typeof(jsonb_extract_path_text_op ('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}','{"f4","f6"}'));