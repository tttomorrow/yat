-- @testpoint: 文本检索操作符!!与@@结合使用2

select to_tsvector('fat cats ate rats') @@(!!'ratt'::tsquery) as result;