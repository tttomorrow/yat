-- @testpoint: Jsonb额外支持的操作符:@>左边的JSON的顶层包含右边JSON的顶层所有JSON项

--1.左右两侧类型相同
select '"ffff"'::jsonb @> '"ffff"'::jsonb;
select '{"a":1, "b": [1,2,3]}'::jsonb @>  '{ "b":    [1,  2,3]}'::jsonb;
select '[null, false,     "test"]'::jsonb @> '["test"         , null ]'::jsonb;
select '[105.2e3, "test", {"a":1}]'::jsonb @> '["test", 1.052e5 , {"a":1},   "test"]'::jsonb;
select '{"a":1 ,"test":[1,2,3], "a":2}'::jsonb @> '{"a":2 ,"test":[1,2,3], "a":2}'::jsonb;
select 'null'::jsonb @> ''::jsonb;

--2.左右两侧类型不相同
select '[{"a":true}, null]'::jsonb @>  'null'::jsonb;
select '[{"a":true}, "null"]'::jsonb @>  '"null"'::jsonb;
select '[ "",  1]'::jsonb @> '""'::jsonb;
select '[105.2e-3, "test "    ]'::jsonb @> '1.0520e-1'::jsonb;
select '["ddd", 1, "ddd"]'::jsonb @> '"ddd"'::jsonb;