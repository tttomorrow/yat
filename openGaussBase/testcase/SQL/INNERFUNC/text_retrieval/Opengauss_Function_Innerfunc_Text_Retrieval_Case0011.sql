-- @testpoint: 文本检索操作符@@，通过to_tsvector函数对单词进行规范化处理，检查词汇类型一致性

select to_tsvector('english', 'the fat rats')@@ 'the'::tsquery  as result;