-- @testpoint: Jsonb额外支持的操作符:@>左边的JSON的顶层不包含右边JSON的顶层所有JSON项

--1.左右两侧类型相同
select '"ffff    "'::jsonb @> '"ffff"'::jsonb;
select '{"true":1, "false":2, "null":null}'::jsonb @> '{"true ":1}'::jsonb;
select '["", -1235e-5]'::jsonb @> '[-1.235e-2,        null]'::jsonb;
select '1230'::jsonb @> '123'::jsonb;
select '["test"         , null ]'::jsonb @> '[null, false,     "test"]'::jsonb;
select '{"a":1 ,"test":[1,2,3], "a":2}'::jsonb @> '{"a":2 ,"test":[1,2,3], "a":1}'::jsonb;

--2.左右两侧类型不相同
select '[{"a":true}, null] '::jsonb @> '"null"'::jsonb;
select '[{"a":true}, null] '::jsonb @> '""'::jsonb;
select '[{"a":true}, null] '::jsonb @> '{}'::jsonb;
select 'null'::jsonb @> '["null"]'::jsonb;