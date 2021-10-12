-- @testpoint: 文本检索操作符&&，当tsquery类型的词汇为空时，进行“与”操作

select 'rat'::tsquery && 'cat'::tsquery && '' ::tsquery  as result;