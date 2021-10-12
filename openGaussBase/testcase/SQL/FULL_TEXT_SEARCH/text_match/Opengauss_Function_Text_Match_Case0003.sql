--  @testpoint:匹配算子符无效性测试
--使用@符号，合理报错
SELECT 'a fat cat sat on a mat and ate a fat rat'::tsvector @ 'cat & rat'::tsquery AS RESULT;
SELECT 'cat rat'::tsvector @ 'cat & rat'::tsquery AS RESULT;
--使用@@@符号（未报错，@@的同义词）
SELECT 'a fat cat sat on a mat and ate a fat rat'::tsvector @@@ 'cat & rat'::tsquery AS RESULT;
SELECT 'cat rat'::tsvector @@@ 'cat & rat'::tsquery AS RESULT;