--  @testpoint:使用等价命令to_tsvector(text) @@ tsquery和to_tsvector(text) @@ plainto_tsquery(text)（返回true）
SELECT to_tsvector('a fat cat sat on a mat and ate a fat rat')@@ 'cat & rat'::tsquery AS RESULT;
--tsvector(document)匹配到一个tsquery(query)(全部匹配)
SELECT to_tsvector('cat rat')@@ 'cat & rat'::tsquery AS RESULT;
--tsvector(document)匹配到一个tsquery(query)，to_tsvector函数标准化会删掉单词末尾s
SELECT to_tsvector('cats rat')@@ 'cat & rat'::tsquery AS RESULT;

--使用等价命令to_tsvector(text) @@ plainto_tsquery(text)
SELECT to_tsvector('a fat cat sat on a mat and ate a fat rat')@@ plainto_tsquery('cat & rat') AS RESULT;
SELECT to_tsvector('cat rat')@@ plainto_tsquery('cat & rat') AS RESULT;
--字串中结尾带s，会删掉s
SELECT to_tsvector('a fat cats sat on a mat and ate a fat rat')@@ plainto_tsquery('cats & rat') AS RESULT;
SELECT to_tsvector('cats rat')@@ plainto_tsquery('cat & rat') AS RESULT;
--plainto_tsquery和to_tsvector顺序颠倒
SELECT  plainto_tsquery('cat & rat') @@ to_tsvector('cats rat') AS RESULT;