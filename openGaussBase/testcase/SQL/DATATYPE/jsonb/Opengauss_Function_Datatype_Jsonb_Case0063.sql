-- @testpoint: 通用函数：json_typeof（返回json的数据类型，当入参不合理时，合理报错）

--json_typeof函数，入参合理
select value, json_typeof(value)  from (values (json '123.4'), (json '"foo"'), (json 'true'), (json 'null'), (json '[1, 2, 3]'), (json '{"x":"foo", "y":123}'), (NULL::json))  as data(value);
select json_typeof('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}');
select json_typeof ('[{"a":"foo"},"b",true,null,138]');
select json_typeof ('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]');
select json_typeof('true');
select json_typeof('138158');
select json_typeof('null');

--json_typeof函数，入参不合理
select json_typeof ('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]','[2,1]');
select json_typeof ('["a","foo","b","bar","c":"baz"]','{"b","c"}');
select json_typeof('true,false');
select json_typeof('138,158,369');
select json_typeof("null");

--返回结果类型校验：text
select pg_typeof(json_typeof('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}'));