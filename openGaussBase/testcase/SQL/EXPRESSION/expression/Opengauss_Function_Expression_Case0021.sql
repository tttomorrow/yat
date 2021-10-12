--  @testpoint: 结合多种表达式的复杂sql

--行表达式和数组表达式
SELECT row(array['2020-11-01'::timestamp,'2020-09-13 00:00:05'::timestamp,'2020-10-04'::timestamp])
= row(array['2020-11-01'::timestamp,'2020-09-13 00:00:05'::timestamp,'2020-10-04'::timestamp]) AS RESULT;

--逻辑表达式和比较表达式
select (1<2 and 'a' > 'b') ISNULL as result;
select (1<2 and 'a' > 'b') IS NOT DISTINCT from false as result;
select (1<2 and 'a' < 'b') between 0 and 1 as result;

--行表达式和逻辑表达式
SELECT ROW(1,2,(1<2 and 'a' > 'b')) < ROW(1,3,(1>2 and 'a' > 'b')) AS RESULT;
SELECT ROW(1,2,(1<2 and 'a' > 'b')) < ROW(1,3,(1>2 and 'a' > 'b'))
and ROW(1,2,(1<2 and 'a' > 'b')) > ROW(1,3,(1>2 and 'a' > 'b'))  AS RESULT;

--条件表达式和比较表达式
SELECT NULLIF('Hello','Hello World') ISNULL as result;
SELECT NULLIF('Hello','Hello') ISNULL as result;
SELECT NULLIF('','Hello') ISNULL as result;

--环境清理
--no need to clean
