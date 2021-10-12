-- @testpoint: jsonb格式校验：Object-jsonb（不符合格式合理报错）

--符合规范
select '{}'::jsonb;
select '{"a": 1, "b": {"a": 2, "b": null}}'::jsonb;
select '{"foo": [true, "bar"], "tags": {"a": 1, "b": null}}'::jsonb;
select '{"a":null, "bb": 1, "bb": "A",   "cde": [1,2,   "re"], "abc": 1}'::jsonb;
select '{"a":null, "[1,2,\"re\"]": 1, "bb": "A", "cde": [1,2,   "re"], "abc": 1}'::jsonb;
--不符合规范
select '{"qq","true","null","false"}'::jsonb;
select '{"a":null, "[1,2,"re"]": 1, "bb": "A", "cde": [1,2,   "re"], "abc": 1}'::jsonb;
select '{"a":null, "[1,2,"re"]": 1},{"bb": "A", "cde": [1,2,"re"], "abc": 1}'::jsonb;
select '"a": 1, "b": {"a": 2, b": null}}'::jsonb;