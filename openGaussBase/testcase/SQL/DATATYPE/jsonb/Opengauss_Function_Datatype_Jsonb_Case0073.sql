-- @testpoint: 通用函数：jsonb_extract_path_text（返回由path_elems指向的JSON值,同操作符 #>>，当入参不合理时，合理报错）

--jsonb_extract_path_text函数，入参合理
select jsonb_extract_path_text('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}', 'f4','f6');
select jsonb_extract_path_text ('{"f1":[1,2,3],"f2":{"f3":1},"f4":null}','f2','f3');
select jsonb_extract_path_text ('{"a":1, "b":"test", "a":2,"b":true}','b','true');
select jsonb_extract_path_text ('{"a": {"b":{"a":{"b":{"a":{"b":88}}}}}}','a','b');
select jsonb_extract_path_text ('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]','2','1');
select jsonb_extract_path_text ('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]','1');

--jsonb_extract_path_text函数，入参不合理
select jsonb_extract_path_text ('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]');
select jsonb_extract_path_text('true','true');
select jsonb_extract_path_text('1389158','138');
select jsonb_extract_path_text('null','n');
select jsonb_extract_path_text('true,false','true');
select jsonb_extract_path_text('138,158,369','138');
select jsonb_extract_path_text('null',);

--返回结果类型校验：text
select pg_typeof(jsonb_extract_path_text ('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}', 'f4','f6'));