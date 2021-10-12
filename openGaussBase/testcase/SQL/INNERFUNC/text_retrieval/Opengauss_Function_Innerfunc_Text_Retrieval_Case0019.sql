-- @testpoint: 文本检索操作符||结合to_tsvector

select  to_tsvector('fat cats ate ate' )|| to_tsvector('tr tre' ) as result;