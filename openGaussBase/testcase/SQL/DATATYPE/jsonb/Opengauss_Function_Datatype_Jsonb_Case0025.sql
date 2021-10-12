-- @testpoint: json操作符：#> 获取在指定路径的JSON对象，路径不存在则返回空，输入不合理时，合理报错

--合理输入1.左侧输入值为object-json类型，右侧为text[]类型
select '{"a": {"b":{"c":{"a":"b"}}}}'::json #>  (select '{a,b}'::text[]);
select '{"a": "b","a":{"a":{"b":88}}}'::json #>  '{a}';
select '{"a": {"b":{"a":{"b":{"a":{"b":88}}}}}}'::json #>  '{b,a}';
select '{"a":"b","a":{"a":{"b":88}},"a":{"a":{"b":99}}}'::json #>  '{a}';
select '{"a":"b","a":{"a":{"b":88}},"a":{"a":{"b":99}}}'::json #> '{a:b}';

--合理输入2.左侧输入值为array-json类型，右侧为text[]类型
select '[1, 2, "foo", null]'::json #> '{2}';
select '[null, 2, "foo", {"b":88}]'::json #> '{3}';
select '[null, 2, "foo", {"b":88}]'::json #> '{2.6}';
select '["a","foo","b","bar","c","baz"]'::json #>  '{a}';

--不合理输入1.左侧输入值为非container-json类型，右侧为text[]类型
select '"a","foo","b","bar","c","baz"'::json #>  '{b,a}';
select '138,852,1323'::json #> (select '{a,b}'::text[]);
select '138'::json #>  '{138}';
select '"ALL"'::json #>  '{A}';
select 'null'::json #> '{n}';
select 'true'::json #> '{t,f}';

--不合理输入2.左侧输入值为非container-json类型，右侧为非text[]类型
select '"a","foo","b","bar","c","baz"'::json #>  'a';
select '138,852,1323'::json #> 2;
select '138'::json #>  '8';
select '"ALL"'::json #> (select '"all"'::json);
select 'null'::json #> '""';
select 'true'::json #> '0';