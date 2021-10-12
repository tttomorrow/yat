-- @testpoint: 文本检索操作符@@，通过to_tsvector函数对单词进行规范化处理，结合正则运算符检查词汇类型一致性

select to_tsvector('fat cats ate fat rats') @@ 'fa:*'::tsquery as result;