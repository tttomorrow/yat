-- @testpoint: 文本检索操作符@@，文本中含有位与运算符 & 时检查词汇类型一致性

select to_tsvector('fat cats ate rats') @@ to_tsquery('rat&catttt') as result;