--  @testpoint: 比较表达式null操作符

--expression IS NULL
select NULL IS NULL AS RESULT;
select 'NULL' IS NULL AS RESULT;
select '' IS NULL AS RESULT;
select ' ' IS NULL AS RESULT;
select 'TEST' IS NULL AS RESULT;

--expression IS NOT NULL
select NULL IS NOT NULL AS RESULT;
select 'NULL' IS NOT NULL AS RESULT;
select '' IS NOT NULL AS RESULT;
select ' ' IS NOT NULL AS RESULT;
select 'TEST' IS NOT NULL AS RESULT;

--expression  ISNULL
select NULL ISNULL AS RESULT;
select 'NULL' ISNULL AS RESULT;
select '' ISNULL AS RESULT;
select ' ' ISNULL AS RESULT;
select 'TEST' ISNULL AS RESULT;

--expression NOTNULL
select NULL NOTNULL AS RESULT;
select 'NULL' NOTNULL AS RESULT;
select '' NOTNULL AS RESULT;
select ' ' NOTNULL AS RESULT;
select 'TEST' NOTNULL AS RESULT;


--建表
drop table if exists test_expression_04 cascade ;
create table test_expression_04(a int, b int);
insert into test_expression_04(a) values(4);
insert into test_expression_04(b) values(4);

select a NOTNULL AS RESULT from test_expression_04;
select a IS NOT NULL AS RESULT from test_expression_04;
select a ISNULL AS RESULT from test_expression_04;
select a IS NULL AS RESULT from test_expression_04;
select b NOTNULL AS RESULT from test_expression_04;
select b IS NOT NULL AS RESULT from test_expression_04;
select b ISNULL AS RESULT from test_expression_04;
select b IS NULL AS RESULT from test_expression_04;

--清理环境
drop table if exists test_expression_04 cascade ;