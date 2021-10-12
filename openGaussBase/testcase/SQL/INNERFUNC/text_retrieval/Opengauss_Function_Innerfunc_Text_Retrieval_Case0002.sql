-- @testpoint: 文本检索操作符@@，检查词汇类型一致性

select to_tsvector('fat cats ate rats') @@ to_tsquery('cat1') as result;