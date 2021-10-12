-- @testpoint: 函数文本检索操作符||，连接两个tsvector类型的词汇

select  'a:1a '::tsvector|| 'b:1a '::tsvector as result;