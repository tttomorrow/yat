-- @testpoint: 通用函数：jsonb_object_keys(获取object-json对应键的值,等效于->>操作符，当入参不合理时，合理报错）

--jsonb_object_keys函数，入参合理
select jsonb_object_keys ('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}');
select jsonb_object_keys ('{"f1":[1,2,3],"f2":{"f3":1},"f4":null}');
select jsonb_object_keys ('{"a":1, "b":"test", "a":2,"b":true}');
select jsonb_object_keys ('{"a": {"b":{"a":{"b":{"a":{"b":88}}}}}}');

--jsonb_object_keys函数，入参不合理
select jsonb_object_keys ('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]');
select jsonb_object_keys ('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]');
select jsonb_object_keys('true');
select jsonb_object_keys('138158');
select jsonb_object_keys('null');

--返回结果类型校验：text
select pg_typeof(jsonb_object_keys ('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}'));