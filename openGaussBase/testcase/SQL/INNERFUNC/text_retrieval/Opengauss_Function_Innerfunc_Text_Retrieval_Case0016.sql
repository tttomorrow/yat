-- @testpoint: 文本检索操作符||，连接两个tsvector类型的词汇

select 'a b'::tsvector || 'c:1 d:2 b:3'::tsvector as result;