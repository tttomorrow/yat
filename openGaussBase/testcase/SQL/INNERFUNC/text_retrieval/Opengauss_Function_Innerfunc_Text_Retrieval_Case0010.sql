-- @testpoint: 文本搜索类型，通过tsvector把一个字符串按照空格进行分词，与@@结合使用

select $$the lexeme '    '  , contains spaces$$::tsvector@@ ','::tsquery  as result;