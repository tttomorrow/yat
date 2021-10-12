-- @testpoint: jsonb格式校验：bool-jsonb（不符合格式合理报错）

--符合格式
select 'false'::jsonb;
select 'true'::jsonb;
--不符合格式
select 'FALSE'::jsonb;
select 'TRUE'::jsonb;