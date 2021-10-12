-- @testpoint: 文本检索操作符&&，@@，to_tsvector函数结合使用

select to_tsvector('fat cats ate rats') @@('rat'::tsquery && 'cat'::tsquery) as result;