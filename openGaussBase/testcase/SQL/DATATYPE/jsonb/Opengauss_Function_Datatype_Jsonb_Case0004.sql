-- @testpoint: openGauss可否正确判断JSON类型:字面值（不符合规范的合理报错）

--符合规范
select 'true'::JSON;
select 'false'::JSON;
select 'null'::JSON;
--不符合规范
select 'TRUE'::JSON;
select 'FALSE'::JSON;
select 'NULL'::JSON;
select 'ALL'::JSON;