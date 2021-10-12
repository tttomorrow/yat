-- @testpoint: 通用函数：jsonb_extract_path（返回由path_elems指向的JSON值,路径不存在则返回空同操作符 #>，当入参不合理时，合理报错）

--jsonb_extract_path函数，入参合理
select jsonb_extract_path('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}', 'f4','f6');
select jsonb_extract_path ('{"f1":[1,2,3],"f2":{"f3":1},"f4":null}','f2','f3');
select jsonb_extract_path ('{"a":1, "b":"test", "a":2,"b":true}','b','true');
select jsonb_extract_path ('{"a": {"b":{"a":{"b":{"a":{"b":88}}}}}}','a','b');
select jsonb_extract_path ('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]','2','1');
select jsonb_extract_path ('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]','1');

--jsonb_extract_path函数，入参不合理
select jsonb_extract_path ('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]');
select jsonb_extract_path('true','true');
select jsonb_extract_path('1389158','138');
select jsonb_extract_path('null','n');
select jsonb_extract_path('true,false','true');
select jsonb_extract_path('138,158,369','138');
select jsonb_extract_path('null',1);

--返回结果类型校验：jsonb
select pg_typeof(jsonb_extract_path ('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}', 'f4','f6'));