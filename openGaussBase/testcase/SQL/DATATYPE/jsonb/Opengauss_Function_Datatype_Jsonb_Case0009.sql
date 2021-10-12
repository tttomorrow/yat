-- @testpoint: json格式校验：bool-json（不符合格式合理报错）

--符合格式
select 'false'::json;
select 'true'::json;
--不符合格式
select 'FALSE'::json;
select 'TRUE'::json;