-- @testpoint: 通用函数：jsonb_array_element（将输入数组中指定元素返回为json对象，同操作符 ->，当入参不合理时，合理报错）

--jsonb_array_element函数，入参合理
select jsonb_array_element('[1,true,[1,[2,3]],null]',2);
select jsonb_array_element('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]',3);
select jsonb_array_element('[138,0.58,-369,1.25e+6]',2.8);
select jsonb_array_element('[138,0.58,-369,1.25e+6]',2.4);
select jsonb_array_element('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]',true);
select jsonb_array_element('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]',false);

--jsonb_array_element函数，入参不合理，合理报错
select jsonb_array_element('["a","foo","b","bar","c","baz"]',"b");
select jsonb_array_element('138,852,1323',1);
select jsonb_array_element('{"a":1,"b":2,"c":3}',1);

--返回结果类型校验：jsonb
select pg_typeof(jsonb_array_element('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]',3));