-- @testpoint: Jsonb额外支持的操作符:<@左边的JSON的所有项全部存在于右边JSON的顶层

--1.左右两侧类型相同
select '"ffff"'::jsonb <@ '"ffff"'::jsonb;
select '{ "b":    [1,  2,3]}'::jsonb <@  '{"a":1, "b": [1,2,3]}'::jsonb;
select '{"a":1 ,"test":[1,2,3], "a":2}'::jsonb <@ '{"a":2 ,"test":[1,2,3], "a":2}'::jsonb;
select 'null'::jsonb <@ ''::jsonb;
select '[105.2e3, "test", {"a":1}]'::jsonb <@ '["test", 1.052e5 , {"a":1},   "test"]'::jsonb;
select '[null,"test"]'::jsonb <@ '["test"         , false,      null ]'::jsonb;
select '{"a":2 ,"test":[1,2,3], "a":2}' <@ '{"a":1 ,"test":[1,2,3], "a":2}'::jsonb;

--2.左右两侧类型不相同
select '[{"a":true}, null]'::jsonb <@  'null'::jsonb;
select '[{"a":true}, "null"]'::jsonb <@  '"null"'::jsonb;
select '[ "",  1]'::jsonb <@ '""'::jsonb;
select '[105.2e-3, "test "    ]'::jsonb <@ '1.0520e-1'::jsonb;
select '["ddd", 1, "ddd"]'::jsonb <@ '"ddd"'::jsonb;