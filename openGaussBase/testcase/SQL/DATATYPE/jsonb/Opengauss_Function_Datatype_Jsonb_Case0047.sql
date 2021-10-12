-- @testpoint: 通用函数：json_array_element（将输入数组中指定元素返回为json对象，同操作符 ->，当入参不合理时，合理报错）

--json_array_element函数，入参合理
select json_array_element('[1,true,[1,[2,3]],null]',2);
select json_array_element('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]',3);
select json_array_element('[138,0.58,-369,1.25e+6]',2.8);
select json_array_element('[138,0.58,-369,1.25e+6]',2.4);
select json_array_element('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]',true);
select json_array_element('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]',false);

--json_array_element函数，入参不合理，合理报错
select json_array_element('["a","foo","b","bar","c","baz"]',"b");
select json_array_element('138,852,1323',1);
select json_array_element('{"a":1,"b":2,"c":3}',1);

--返回结果类型校验：json
select pg_typeof(json_array_element('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]',3));