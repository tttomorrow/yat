-- @testpoint: 通用函数：json_object_field_text(获取object-json对应键的值,等效于->>操作符，当入参不合理时，合理报错）

--json_object_field_text函数，入参合理
select json_object_field_text ('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}','f4');
select json_object_field_text ('{"f1":[1,2,3],"f2":{"f3":1},"f4":null}','f3');
--对于重复的键，json由于储存的是精确的输入拷贝，所以输出时仍会显示出来，但是用json执行部分操作计算时，会按照最后出现的计算，如查找对应键的值
select json_object_field_text ('{"a":2, "b":"test", "a":1,"b":true}','a');
select json_object_field_text ('{"a": {"b":{"a":{"b":{"a":{"b":88}}}}}}','a');

--json_object_field_text函数，入参不合理
select json_object_field_text ('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]','b');
select json_object_field_text ('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]','2');
select json_object_field_text('true','1');
select json_object_field_text('138158','138');
select json_object_field_text('null','n');

--返回结果类型校验：text
select pg_typeof(json_object_field_text ('{"a": {"b":{"a":{"b":{"a":{"b":88}}}}}}','a'));