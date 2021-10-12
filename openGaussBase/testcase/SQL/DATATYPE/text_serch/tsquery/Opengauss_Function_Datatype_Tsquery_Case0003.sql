-- @testpoint: 前缀首先被文本搜索分词器处理

select to_tsvector( 'postgraduate' ) @@ to_tsquery( 'postgres:*' ) as result;