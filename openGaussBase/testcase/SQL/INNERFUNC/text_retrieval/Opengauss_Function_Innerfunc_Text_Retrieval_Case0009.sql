-- @testpoint: 文本检索操作符@@，与tsvector和tsquery结合使用

select 'a:1 fat:2 cat:3 sat:4 on:5'::tsvector @@ 'fat'::tsquery  as result;