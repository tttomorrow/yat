-- @testpoint: jsonb操作符：-> 通过object-jsonb的键获得值，不存在返回空，输入不合理时，合理报错

--合理输入1.左侧输入值为object-jsonb类型，右侧为text类型
select '{"a": 1, "b": {"a": 2, "b": null}}'::jsonb -> 'b' ;
select '{"foo": [true, "bar"], "tags": {"a": 1, "b": null}}'::jsonb  -> 'tags';
select '{"a":null, "bb": 1, "bb": "A",   "cde": [1,2,   "re"], "abc": 1}'::jsonb  -> 'bb';
select '{"a":null, "[1,2,\"re\"]": 1, "bb": "A", "cde": [1,2,   "re"], "abc": 1}'::jsonb  -> 'abcd';

--合理输入2.左侧输入键的值为空的object-jsonb类型，右侧为text类型
select '{}'::jsonb  ->'';
select '{"":true}'::jsonb -> '';
select '{"":"qwe"}'::jsonb -> '""';
select '{" ":"qwe"}'::jsonb -> ' ';

--不合理输入1.左侧输入值为object-jsonb类型，右侧为非text类型
select '{}'::jsonb -> 2;
select '{"a": 1, "b": {"a": 2, "b": null}}'::jsonb  -> a;
select '{"a": 1, "b": {"a": 2, "b": null}}'::jsonb  -> 2021-05-31 12:59:08;
select '{"foo": [true, "bar"], "tags": {"a": 1, "b": null}}'::jsonb -> 192.168.100.128/25;
select '{"a":null, "bb": 1, "bb": "A",   "cde": [1,2,   "re"], "abc": 1}':: -> true;
select '{"a":null, "[1,2,\"re\"]": 1, "bb": "A", "cde": [1,2,   "re"], "abc": 1}':: -> null;

--不合理输入2.左侧输入值为非object-jsonb类型，右侧为text类型
select '138,852,1323'::jsonb -> '138';
select '"ALL"'::jsonb -> 'all';
select '+100'::jsonb -> '1';
select '[{"a":"foo"},{"b":"bar"},{"c":"baz"}]'::jsonb -> 'a';

--不合理输入3.左侧输入值为非object-jsonb类型，右侧为非text类型
select 'abcdefg'::jsonb -> ab;
select '''abcdefg'''::jsonb -> 2021-05-31;
select '\"$$\"'::jsonb ->192.168.100.128/25;
select '"["www@13^", 1, {"name": "john"}, "2"]"'::jsonb -> 1/2;