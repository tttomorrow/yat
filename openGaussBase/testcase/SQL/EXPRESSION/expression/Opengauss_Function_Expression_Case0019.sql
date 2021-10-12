--  @testpoint: ALL (array)
--右侧括号中的是一个数组表达式，它必须产生一个数组值。左侧表达式的结果使用操作符对数组表达式的每一行结果都进行计算和比较，比较结果必须是布尔值。
--•如果所有的比较结果都为真值（包括数组不含任何元素的情况），则ALL的结果为true。
--•如果存在一个或多个比较结果为假值，则ALL的结果为false。
--如果数组表达式产生一个NULL数组，则ALL的结果为NULL。
--如果左边表达式的值为NULL ，则ALL的结果通常也为NULL(某些不严格的比较操作符可能得到不同的结果)。
--另外，如果右边的数组表达式中包含null元素并且比较结果没有假值，则ALL的结果将是NULL(某些不严格的比较操作符可能得到不同的结果)， 而不是真。
--这样的处理方式和SQL返回空值的布尔组合规则是一致的。

--全真（包括数组不含任何元素的情况）则为真
SELECT 9000+500 < ALL (array[10000, 9800]) AS RESULT;
SELECT 9000+500 <= ALL (array[10000, 9500]) AS RESULT;
SELECT 9000+500 != ALL (array[10000, 9000]) AS RESULT;
SELECT 9000+500 >= ALL (array[1000, 9000]) AS RESULT;
SELECT 'test' != ALL (array['hello', 'world']) AS RESULT;
SELECT ADD_MONTHS('2020-10-13',1) > ALL (array['2020-10-01'::timestamp,'2020-09-13 00:00:05'::timestamp,'2020-10-04'::timestamp]) AS RESULT;

--一假则为假，覆盖常用操作符
SELECT 9000+500 < ALL (array[10000, 9000]) AS RESULT;
SELECT 9000+500 <= ALL (array[10000, 9800]) AS RESULT;
SELECT 9000+500 != ALL (array[10000, 9500]) AS RESULT;
SELECT 9000+500 >= ALL (array[1000, 9900]) AS RESULT;
SELECT 'test' != ALL (array['test','hello', 'world']) AS RESULT;
SELECT ADD_MONTHS('2020-10-13',1) > ALL (array['2020-11-01'::timestamp,'2020-09-13 00:00:05'::timestamp,'2020-10-04'::timestamp]) AS RESULT;

--数组表达式产生一个NULL数组，则ALL的结果为NULL
SELECT 9000+500 < ALL (array[null, null,null]) AS RESULT;
SELECT 9000+500 <= ALL (array[null, null,null]) AS RESULT;
SELECT 9000+500 != ALL (array[null, null,null]) AS RESULT;
SELECT 9000+500 >= ALL (array[null, null,null]) AS RESULT;
SELECT 'test' != ALL (array[null,null,null,null]) AS RESULT;

--左边表达式的值为NULL ，ALL的结果通常为NULL（某些不严格的比较操作符可能得到不同的结果）
SELECT null < ALL (array[10000, 9800]) AS RESULT;
SELECT null <= ALL (array[10000, 9500]) AS RESULT;
SELECT null != ALL (array[10000, 9000]) AS RESULT;
SELECT null >= ALL (array[1000, 9000]) AS RESULT;
SELECT null != ALL (array['hello', 'world']) AS RESULT;

--右边的数组表达式中包含null且比较结果全真，则ALL的结果是NULL(某些不严格的比较操作符可能得到不同的结果)
SELECT 9000+500 < ALL (array[10000, 9800,null]) AS RESULT;
SELECT 9000+500 <= ALL (array[10000, 9500,null]) AS RESULT;
SELECT 9000+500 != ALL (array[10000, 9000,null]) AS RESULT;
SELECT 9000+500 >= ALL (array[1000, 9000,null]) AS RESULT;
SELECT 'test' != ALL (array['hello', 'world',null]) AS RESULT;

--环境清理
--no need to clean