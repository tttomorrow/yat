-- @testpoint: 通用函数：json(b)_typeof（返回json的数据类型，当入参不合理时，合理报错）

--jsonb_typeof函数，入参合理
select value, jsonb_typeof(value)  from (values (jsonb '123.4'), (jsonb '"foo"'), (jsonb 'true'), (jsonb 'null'), (jsonb '[1, 2, 3]'), (jsonb '{"x":"foo", "y":123}'), (NULL::jsonb))  as data(value);
select jsonb_typeof('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}');
select jsonb_typeof ('[{"a":"foo"},"b",true,null,138]');
select jsonb_typeof ('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]');
select jsonb_typeof('true');
select jsonb_typeof('138158');
select jsonb_typeof('null');

--jsonb_typeof函数，入参不合理
select jsonb_typeof ('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]','[2,1]');
select jsonb_typeof ('["a","foo","b","bar","c":"baz"]','{"b","c"}');
select jsonb_typeof('true,false');
select jsonb_typeof('138,158,369');
select jsonb_typeof("null");

--返回结果类型校验：text
select pg_typeof(jsonb_typeof ('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}'));
