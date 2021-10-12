--  @testpoint:tsquery类型的查询，相关函数测试
--tsquery && tsquery
SELECT 'fat | rat'::tsquery && 'cat'::tsquery AS RESULT;
SELECT 'fat & rat'::tsquery && 'cat'::tsquery AS RESULT;
--tsquery || tsquery
SELECT 'fat | rat'::tsquery || 'cat'::tsquery AS RESULT;
SELECT 'fat & rat'::tsquery || 'cat'::tsquery AS RESULT;
--!! tsquery
SELECT !! 'cat'::tsquery AS RESULT;
SELECT !! 'cat & dog'::tsquery AS RESULT;

