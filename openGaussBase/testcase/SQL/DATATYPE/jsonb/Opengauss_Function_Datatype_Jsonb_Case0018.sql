-- @testpoint: jsonb操作符：-> 获得array-jsonb元素，下标不存在返回空，输入不合理时，合理报错

--合理输入1.左侧输入值为array-jsonb类型，右侧为int类型
select '[{"a":"foo"},{"b":"bar"},{"c":"baz"}]'::jsonb -> 0;
select '["a","foo","b","bar","c","baz"]'::jsonb -> 2.1;
select '["a","foo","b","bar","c","baz"]'::jsonb -> 2.7;
select '[null,true,false,"null","true","false"]'::jsonb -> -5.5;
select '[138,0.58,-369,1.25e+6]'::jsonb -> 1/3;

--合理输入2.左侧输入值为空的array-jsonb类型，右侧为int类型
select '[]'::jsonb -> 0;
select '[""]'::jsonb -> 1;
select '[null]'::jsonb -> 2;

--合理输入3.左侧输入值为array-jsonb类型，右侧为可隐式转换为int类型的类型
select '[{"a":"foo"},{"b":"bar"},{"c":"baz"}]'::jsonb -> true;
select '[{"a":"foo"},{"b":"bar"},{"c":"baz"}]'::jsonb -> false;
select '[{"a":"foo"},{"b":"bar"},{"c":"baz"}]'::jsonb -> null;

--不合理输入1.左侧输入值为array-jsonb类型，右侧为非int类型
select '["a","foo","b","bar","c","baz"]'::jsonb -> "b" ;
select '[null,true,false,"null","true","false"]'::jsonb -> 2021-05-31 12:59:08;
select '[138,0.58,-369,1.25e+6]'::jsonb -> 192.168.100.128/25;

--不合理输入2.左侧输入值为非array-jsonb类型，右侧为int类型
select '138,852,1323'::jsonb -> 1;
select '"ALL"'::jsonb -> 0;
select '+100'::jsonb -> -2;

--不合理输入3.左侧输入值为非array-jsonb类型，右侧为非int类型
select 'abcdefg'::jsonb -> 'ab';
select '''abcdefg'''::jsonb -> 2021-05-31;
select '\"$$\"'::jsonb ->192.168.100.128/25;
select '"["www@13^", 1, {"name": "john"}, "2"]"'::jsonb -> 1/2;