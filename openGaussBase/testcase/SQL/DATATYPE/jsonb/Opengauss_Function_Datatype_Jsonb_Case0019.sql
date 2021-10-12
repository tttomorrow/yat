-- @testpoint: json操作符：-> 通过object-json的键获得值，不存在返回空，输入不合理时，合理报错

--合理输入1.左侧输入值为object-json类型，右侧为text类型
select '{"a": 1, "b": {"a": 2, "b": null}}'::json -> 'b' ;
select '{"foo": [true, "bar"], "tags": {"a": 1, "b": null}}'::json  -> 'tags';
select '{"a":null, "bb": 1, "bb": "A",   "cde": [1,2,   "re"], "abc": 1}'::json  -> 'bb';
select '{"a":null, "[1,2,\"re\"]": 1, "bb": "A", "cde": [1,2,   "re"], "abc": 1}'::json  -> 'abcd';

--合理输入2.左侧输入键的值为空的object-json类型，右侧为text类型
select '{}'::json  ->'';
select '{"":true}'::json -> '';
select '{"":"qwe"}'::json -> '""';
select '{" ":"qwe"}'::json -> ' ';

--不合理输入1.左侧输入值为object-json类型，右侧为非text类型
select '{}'::json -> 2;
select '{"a": 1, "b": {"a": 2, "b": null}}'::json  -> a;
select '{"a": 1, "b": {"a": 2, "b": null}}'::json  -> 2021-05-31 12:59:08;
select '{"foo": [true, "bar"], "tags": {"a": 1, "b": null}}'::json -> 192.168.100.128/25;
select '{"a":null, "bb": 1, "bb": "A",   "cde": [1,2,   "re"], "abc": 1}':: -> true;
select '{"a":null, "[1,2,\"re\"]": 1, "bb": "A", "cde": [1,2,   "re"], "abc": 1}':: -> null;

--不合理输入2.左侧输入值为非object-json类型，右侧为text类型
select '138,852,1323'::json -> '138';
select '"ALL"'::json -> 'all';
select '+100'::json -> '1';
select '[{"a":"foo"},{"b":"bar"},{"c":"baz"}]'::jsonb -> 'a';

--不合理输入3.左侧输入值为非object-json类型，右侧为非text类型
select 'abcdefg'::json -> ab;
select '''abcdefg'''::json -> 2021-05-31;
select '\"$$\"'::json ->192.168.100.128/25;
select '"["www@13^", 1, {"name": "john"}, "2"]"'::json -> 1/2;