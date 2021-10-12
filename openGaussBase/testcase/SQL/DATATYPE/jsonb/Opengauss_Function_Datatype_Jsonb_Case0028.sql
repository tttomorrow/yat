-- @testpoint: jsonb操作符：#>> 获取在指定路径的JSON对象，路径不存在则返回空，输入不合理时，合理报错

--合理输入1.左侧输入值为object-jsonb类型，右侧为text[]类型
select '{"a": {"b":{"c":{"a":"b"}}}}'::jsonb #>> (select '{a,b}'::text[]);
select '{"a": "b","a":{"a":{"b":88}}}'::jsonb #>> '{a}';
select '{"a": {"b":{"a":{"b":{"a":{"b":88}}}}}}'::jsonb #>> '{b,a}';
select '{"a":"b","a":{"a":{"b":88}},"a":{"a":{"b":99}}}'::jsonb #>> '{a}';
select '{"a":"b","a":{"a":{"b":88}},"a":{"a":{"b":99}}}'::jsonb #>> '{a:b}';

--合理输入2.左侧输入值为array-jsonb类型，右侧为text[]类型
select '[1, 2, "foo", null]'::jsonb #>> '{2}';
select '[null, 2, "foo", {"b":88}]'::jsonb #>> '{3}';
select '[null, 2, "foo", {"b":88}]'::jsonb #>> '{2.6}';
select '["a","foo","b","bar","c","baz"]'::jsonb #>> '{a}';

--不合理输入1.左侧输入值为非container-jsonb类型，右侧为text[]类型
select '"a","foo","b","bar","c","baz"'::jsonb #>>  '{b,a}';
select '138,852,1323'::jsonb #>> (select '{a,b}'::text[]);
select '138'::jsonb #>>  '{138}';
select '"ALL"'::jsonb #>>  '{A}';
select 'null'::jsonb #>> '{n}';
select 'true'::jsonb #>> '{t,f}';

--不合理输入2.左侧输入值为非container-jsonb类型，右侧为非text[]类型
select '"a","foo","b","bar","c","baz"'::json #>>  'a';
select '138,852,1323'::jsonb #>> 2;
select '138'::jsonb #>>  '8';
select '"ALL"'::jsonb #>> (select '"all"'::json);
select 'null'::jsonb #>> '""';
select 'true'::jsonb #>> '0';