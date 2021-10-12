-- @testpoint: 通用函数：json_array_length（返回最外层数组中的元素数量，当入参不合理时，合理报错）

--json_array_length函数，入参合理
select json_array_length('[1,true,[1,[2,3]],null,"test"]');
select json_array_length('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]');
select json_array_length('[138,0.58,-369,1.25e+6]');
select json_array_length('["a","foo","b","bar","c","baz"]');

--json_array_length函数，入参不合理，合理报错
select json_array_length('1,true,"[1,[2,3]]",null,"test","b"');
select json_array_length('false,138,852,1323');
select json_array_length('null');
select json_array_length('{"a":1,"b":2,"c":3}');

----返回结果类型检验：int
select pg_typeof(json_array_length('[1,true,[1,[2,3]],null,"test"]'));