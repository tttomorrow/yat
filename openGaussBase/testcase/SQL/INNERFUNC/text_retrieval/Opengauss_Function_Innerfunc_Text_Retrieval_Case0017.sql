-- @testpoint: 文本检索操作符||，通过tsvector把字符串按照空格分割

select $$the lexeme '    '  , contains spaces$$::tsvector || 'c:1 d:2 b:3'::tsvector as result;