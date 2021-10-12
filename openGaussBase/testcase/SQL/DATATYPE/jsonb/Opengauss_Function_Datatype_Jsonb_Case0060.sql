-- @testpoint: 通用函数：json_object_keys(获取object-json对应键的值,等效于->>操作符，当入参不合理时，合理报错）

--json_object_keys函数，入参合理
select json_object_keys ('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}');
select json_object_keys ('{"f1":[1,2,3],"f2":{"f3":1},"f4":null}');
--对于重复的键，json由于储存的是精确的输入拷贝，所以输出时仍会显示出来，但是用json执行部分操作计算时，会按照最后出现的计算，如查找对应键的值
select json_object_keys ('{"a":2, "b":"test", "a":1,"b":true,"c":null}');
select json_object_keys ('{"a": {"b":{"a":{"b":{"a":{"b":88}}}}}}');

--json_object_keys函数，入参不合理
select json_object_keys ('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]');
select json_object_keys ('[{"a":"foo"},{"b":"bar"},{"c":"baz"}]');
select json_object_keys('true');
select json_object_keys('138158');
select json_object_keys('null');

--返回结果类型校验：text
select pg_typeof(json_object_keys ('{"a": {"b":{"a":{"b":{"a":{"b":88}}}}}}'));