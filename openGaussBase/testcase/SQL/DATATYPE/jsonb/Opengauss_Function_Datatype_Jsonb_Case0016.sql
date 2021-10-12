-- @testpoint: json格式校验：Object-json（不符合格式合理报错）

--符合规范
select '{}'::json;
select '{"a": 1, "b": {"a": 2, "b": null}}'::json;
select '{"foo": [true, "bar"], "tags": {"a": 1, "b": null}}'::json;
select '{"a":null, "bb": 1, "bb": "A",   "cde": [1,2,   "re"], "abc": 1}'::json;
select '{"a":null, "[1,2,\"re\"]": 1, "bb": "A", "cde": [1,2,   "re"], "abc": 1}'::json;
--不符合规范
select '{"qq","true","null","false"}'::json;
select '{"a":null, "[1,2,"re"]": 1, "bb": "A", "cde": [1,2,   "re"], "abc": 1}'::json;
select '{"a":null, "[1,2,"re"]": 1},{"bb": "A", "cde": [1,2,"re"], "abc": 1}'::json;
select '"a": 1, "b": {"a": 2, b": null}}'::json;"