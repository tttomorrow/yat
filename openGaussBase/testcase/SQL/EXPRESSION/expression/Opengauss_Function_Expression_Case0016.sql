--  @testpoint: IN
--右侧括号中的是一个表达式列表。
--左侧表达式的结果与表达式列表的内容进行比较。
--如果列表中的内容符合左侧表达式的结果，则IN的结果为true。
--如果没有相符的结果，则IN的结果为false。

--一般常用的数值，日期，和字符表达式，与函数结合
SELECT 8000+500 IN (10000, 9000) AS RESULT;
SELECT 'hello'::TEXT || ' world'::TEXT IN ('hello world', 'hello','world') AS RESULT;
SELECT ADD_MONTHS('2020-10-13',1) IN ('2020-11-01'::timestamp,'2020-11-13 00:00:05'::timestamp,'2020-11-04'::timestamp) AS RESULT;

--表达式结果为null，IN返回NULL
SELECT null IN (10000, 9000) AS RESULT;

--表达式列表不符合表达式的条件且右侧表达式列表返回结果至少一处为空，IN返回NULL
SELECT  8000+500 IN (10000, 9000, null) AS RESULT;

--表达式列表符合表达式的条件且右侧表达式列表返回结果至少一处为空，IN返回TRUE
SELECT  8000+2000 IN (10000, 9000, null) AS RESULT;

--表达式列表不符合表达式的条件且右侧表达式列表返回结果均不为空，IN返回FALSE
SELECT  8000+200 IN (10000, 9000) AS RESULT;

--环境清理
--no need to clean