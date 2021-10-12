-- @testpoint: json操作符：-> 获得array-json元素，下标不存在返回空，输入不合理时，合理报错

--合理输入1.左侧输入值为array-json类型，右侧为int类型
select '[{"a":"foo"},{"b":"bar"},{"c":"baz"}]'::json -> 0;
select '["a","foo","b","bar","c","baz"]'::json -> 2.1;
select '["a","foo","b","bar","c","baz"]'::json -> 2.7;
select '[null,true,false,"null","true","false"]'::json -> -5.5;
select '[138,0.58,-369,1.25e+6]'::json -> 1/3;

--合理输入2.左侧输入值为空的array-json类型，右侧为int类型
select '[]'::json -> 0;
select '[""]'::json -> 1;
select '[null]'::json -> 2;

--合理输入3.左侧输入值为array-json类型，右侧为可隐式转换为int类型的类型
select '[{"a":"foo"},{"b":"bar"},{"c":"baz"}]'::json -> true;
select '[{"a":"foo"},{"b":"bar"},{"c":"baz"}]'::json -> false;
select '[{"a":"foo"},{"b":"bar"},{"c":"baz"}]'::json -> null;

--不合理输入1.左侧输入值为array-json类型，右侧为非int类型
select '["a","foo","b","bar","c","baz"]'::json -> "b" ;
select '[null,true,false,"null","true","false"]'::json -> 2021-05-31 12:59:08;
select '[138,0.58,-369,1.25e+6]'::json -> 192.168.100.128/25;

--不合理输入2.左侧输入值为非array-json类型，右侧为int类型
select '138,852,1323'::json -> 1;
select '"ALL"'::json -> 0;
select '+100'::json -> -2;

--不合理输入3.左侧输入值为非array-json类型，右侧为非int类型
select 'abcdefg'::json -> 'ab';
select '''abcdefg'''::json -> 2021-05-31;
select '\"$$\"'::json ->192.168.100.128/25;
select '"["www@13^", 1, {"name": "john"}, "2"]"'::json -> 1/2;