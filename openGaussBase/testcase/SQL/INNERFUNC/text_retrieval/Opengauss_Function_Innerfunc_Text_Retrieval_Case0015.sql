-- @testpoint: 文本检索操作符||，连接两个tsvector类型的词汇

select 'fat cats ate'::tsvector || 'a b c'::tsvector;