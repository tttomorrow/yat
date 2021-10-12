-- @testpoint: 文本检索操作符@>，检查一个tsquery类型的词汇是否包含另一个tsquery类型的词汇1

select 'cat'::tsquery @> 'cat & rat'::tsquery as result;