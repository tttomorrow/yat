-- @testpoint: Jsonb额外支持的操作符:<@左边的JSON的所有项是否存在于右边JSON的顶层，右侧不为jsonb，合理报错

--当右侧不为jsonb
select '"ffff"'::jsonb <@ '"ffff"'::json;
select 'null'::jsonb <@ 'null'::json;
select 'null'::jsonb <@ ''::json;
select 'true'::jsonb <@ 'true'::json;
select '{"a":1, "b": [1,2,3]}'::jsonb <@  '{ "b":    [1,  2,3]}'::json;
select '[null, false,     "test"]'::jsonb <@ '["test"     , null ]'::json;
select '105.2e3'::jsonb <@ '1.052e5'::json;
select '[{"a":true}, null] '::  jsonb <@ "null";
select '[{"a":true}, null] '::  jsonb <@ [null];
select '[{"a":true}, null] '::  jsonb <@ '{a:true}';