-- @testpoint: json格式校验：Null-json（不符合格式合理报错）

--json格式校验：Null-json
--符合格式
--1.Null-json格式
select 'null'::json;
--2.空值
select ''::json;
select null::json;
--3.字符串null
select '"null"'::json;
--4.空字符串""
select '""'::json;
--不符合格式
select 'NULL'::json;
select ''null''::json;
select '''null'''::json;