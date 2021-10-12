-- @testpoint: Jsonb额外支持的操作符:= 判断两个jsonb的大小是否相等

--同类型
select '"str"'::jsonb =  '"string"'::jsonb;
select 'null'::jsonb = 'null' ::jsonb;
select 'false'::jsonb = 'false'::jsonb;
select 'false'::jsonb = 'true'::jsonb;
select '{"a":1, "b": [10,2,3],"c":{"b":"d"}}'::jsonb = '{"b":[10,2,3]}'::jsonb;
select '[null, false, 123,{"a":true},"test"]'::jsonb = '[123,{"a":false},"test",null, false]'::jsonb;
select '105.2e-3'::jsonb = '1.0520e-1'::jsonb;

--不同类型
select '"str"'::jsonb =  'null'::jsonb;
select 'null'::jsonb = 'true' ::jsonb;
select 'null'::jsonb = '0' ::jsonb;
select 'null'::jsonb =  '{"b":[10,2,3]}'::jsonb;
select 'null'::jsonb = '[12,"test",null, false]'::jsonb;
select 'true'::jsonb = '1'::jsonb;
select '{"a":1, "b": [10,2,3],"c":{"b":"d"}}'::jsonb = '[{"b":[10,2,3]},{"a":1},{"c":{"b":"d"}}]'::jsonb;
select '[{"a":false},{"a":true}]'::jsonb = '{"a": true,"a": false}'::jsonb;
select '105.2e3'::jsonb = '"0.1052"'::jsonb;
select '0'::jsonb = 'false'::jsonb;
select '258'::jsonb = '{"a":258}'::jsonb;
select '0.369'::jsonb = '[0.369]'::jsonb;
select '"true"'::jsonb = 'true' ::jsonb;
select '"true"'::jsonb = '{"a":"true"}' ::jsonb;
select '"true"'::jsonb = '["true"]' ::jsonb;
select '{"a":1, "b": [10,2,3],"c":{"b":"d"}}'::jsonb = 'true'::jsonb;
select '[{"a":false},{"a":true}]'::jsonb = 'false'::jsonb;