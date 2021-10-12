-- @testpoint: 文本检索操作符||，将两个tsquery类型的词汇进行“或”操作

select 'fat & rat'::tsquery || 'cat'::tsquery as result;