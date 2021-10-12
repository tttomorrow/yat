-- @testpoint: 通用函数：json_extract_path（返回由path_elems指向的JSON值,路径不存在则返回空同操作符 #>，当入参不合理时，合理报错）

--json_extract_path函数，入参合理
select json_extract_path('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}', 'f4','f6');
select json_extract_path ('{"f1":[1,2,3],"f2":{"f3":1},"f4":null}','f2','f3');
select json_extract_path ('{"a":1, "b":"test", "a":2,"b":true}','a','0');
select json_extract_path ('{"a": {"b":{"a":{"b":{"a":{"b":88}}}}}}','a','b');
select json_extract_path ('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]','2','1');
select json_extract_path ('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]','2');
select json_extract_path('true','1');
select json_extract_path('138158','138');
select json_extract_path('null','n');

--json_extract_path函数，入参不合理
select json_extract_path ('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]','2','1');
select json_extract_path ('"a","foo","b","bar","c":"baz"','b','c');
select json_extract_path('true,false','true');
select json_extract_path('138,158,369','138');
select json_extract_path('null');

--返回结果类型校验：json
select pg_typeof(json_extract_path ('{"a": {"b":{"a":{"b":{"a":{"b":88}}}}}}','a','b'));