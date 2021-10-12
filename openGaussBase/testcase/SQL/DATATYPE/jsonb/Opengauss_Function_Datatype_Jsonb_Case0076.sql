-- @testpoint: 通用函数：jsonb_object_field_text(获取object-json对应键的值,等效于->>操作符，当入参不合理时，合理报错）

--jsonb_object_field_text函数，入参合理
select jsonb_object_field_text ('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}','f4');
select jsonb_object_field_text ('{"f1":[1,2,3],"f2":{"f3":1},"f4":null}','f3');
select jsonb_object_field_text ('{"a":1, "b":"test", "a":2,"b":true}','a');
select jsonb_object_field_text ('{"a": {"b":{"a":{"b":{"a":{"b":88}}}}}}','a');

--jsonb_object_field_text函数，入参不合理
select jsonb_object_field_text ('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]','b');
select jsonb_object_field_text ('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]','2');
select jsonb_object_field_text('true','1');
select jsonb_object_field_text('138158','138');
select jsonb_object_field_text('null','n');

--返回结果类型校验：text
select pg_typeof(jsonb_object_field_text ('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}','f4'));