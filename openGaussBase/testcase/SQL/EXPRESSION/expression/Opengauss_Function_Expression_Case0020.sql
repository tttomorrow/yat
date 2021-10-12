-- @testpoint: 行表达式 合理报错
--row_constructor operator row_constructor
--两边都是一个行构造器，两行值必须具有相同数目的字段，每一行都进行比较，行比较允许使用=，<>，<，<=，>=等操作符，或其中一个相似的语义符。
--=<>和别的操作符使用略有不同。如果两行值的所有字段都是非空并且相等，则认为两行是相等的；
--如果两行值的任意字段为非空并且不相等，则认为两行是不相等的；否则比较结果是未知的（null）。
--对于<，<=，>，> =的情况下，行中元素从左到右依次比较，直到遇到一对不相等的元素或者一对为空的元素。
--如果这对元素中存在至少一个null值，则比较结果是未知的（null），否则这对元素的比较结果为最终的结果。

--构造两行数据覆盖<，<=，>,>=表达式，和常用数据类型
SELECT ROW(1,2,NULL) < ROW(1,3,0) AS RESULT;
SELECT ROW(1,2,NULL) <= ROW(1,3,0) AS RESULT;
SELECT ROW(1,2,NULL) = ROW(1,3,0) AS RESULT;
SELECT ROW(1,2,NULL) > ROW(1,3,0) AS RESULT;
SELECT ROW(1,2,NULL) >= ROW(1,3,0) AS RESULT;
SELECT 'test' != ALL (array['test','hello', 'world']) AS RESULT;
SELECT row(array['2020-11-01'::timestamp,'2020-09-13 00:00:05'::timestamp,'2020-10-04'::timestamp])
= row(array['2020-11-01'::timestamp,'2020-09-13 00:00:05'::timestamp,'2020-10-04'::timestamp]) AS RESULT;
SELECT row('2020-11-01'::timestamp,'2020-09-13 00:00:05'::timestamp,'2020-10-04'::timestamp)
= row('2020-11-01'::timestamp,'2020-09-13 00:00:05'::timestamp,'2020-10-04'::timestamp) AS RESULT;

--=<>，非空相等则相等，非空不等则不等
SELECT ROW(null,2) = ROW(1,3) AS RESULT;
SELECT ROW(null,2) <> ROW(1,3) AS RESULT;
--否则返回NULL
SELECT ROW(null,2) = ROW(1,2) AS RESULT;
SELECT ROW(null,2) != ROW(1,2) AS RESULT;

--null
SELECT ROW(null) != ROW(1) AS RESULT;
SELECT ROW(null) != ROW(null) AS RESULT;

--非空情况下数值类型<，<=，>，>=确认比较顺序


--左右数量异常：合理报错
SELECT ROW(null) != ROW(null,1) AS RESULT;
SELECT ROW(1,2,NULL) < ROW(3,0) AS RESULT;

--环境清理
--no need to clean