-- @testpoint: 通用函数：jsonb_array_elements_text（将array_json顶层的每一项拆成一行，当入参不合理时，合理报错）

--jsonb_array_elements_text函数，入参合理
select jsonb_array_elements_text('[1,true,[1,[2,3]],null,"test"]');
select jsonb_array_elements_text('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]');
select jsonb_array_elements_text('[138,0.58,-369,1.25e+6]');
select jsonb_array_elements_text('["a","foo","b","bar","c","baz"]');


--jsonb_array_elements_text函数，入参不合理，合理报错
select jsonb_array_elements_text('1,true,"[1,[2,3]]",null,"test","b"');
select jsonb_array_elements_text('false,138,852,1323');
select jsonb_array_elements_text('null');
select jsonb_array_elements_text('{"a":1,"b":2,"c":3}');

----返回结果类型检验：Setof text
select pg_typeof(jsonb_array_elements_text('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]'));