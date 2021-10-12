-- @testpoint: jsonb格式校验：Null-jsonb（不符合格式合理报错）

--jsonb格式校验：Null-jsonb
--符合格式
--1.Null-jsonb格式
select 'null'::jsonb;
--2.空值
select ''::jsonb;
select null::jsonb;
--3.字符串null
select '"null"'::jsonb;
--4.空字符串""
select '""'::jsonb;
--不符合格式
select 'NULL'::jsonb;
select ''null''::jsonb;
select '''null'''::jsonb;