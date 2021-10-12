--  @testpoint:匹配算子@@测试（返回false或空值)
--tsvector(document)匹配不上一个tsquery(query)
SELECT 'a fat cats sat on a mat and ate a fat rats'::tsvector @@ 'cat & rat'::tsquery AS RESULT;
--tsvector(document)为空
SELECT ''::tsvector @@ 'cat & rat'::tsquery AS RESULT;
--tsquery(query)为空
SELECT 'a fat cats sat on a mat and ate a fat rats'::tsvector @@ ''::tsquery AS RESULT;
