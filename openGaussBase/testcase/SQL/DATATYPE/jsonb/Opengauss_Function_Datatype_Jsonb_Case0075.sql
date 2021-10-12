-- @testpoint: 通用函数：jsonb_object_field(获取object-json对应键的值,等效于->操作符，当入参不合理时，合理报错）

--jsonb_object_field函数，入参合理
select jsonb_object_field ('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}','f4');
select jsonb_object_field ('{"f1":[1,2,3],"f2":{"f3":1},"f4":null}','f3');
select jsonb_object_field ('{"a":1, "b":"test", "a":2,"b":true}','a');
select jsonb_object_field ('{"a": {"b":{"a":{"b":{"a":{"b":88}}}}}}','a');

--jsonb_object_field函数，入参不合理
select jsonb_object_field ('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]','b');
select jsonb_object_field ('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]','2');
select jsonb_object_field('true','1');
select jsonb_object_field('138158','138');
select jsonb_object_field('null','n');

--返回结果类型校验：jsonb
select pg_typeof(jsonb_object_field ('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}','f4'));