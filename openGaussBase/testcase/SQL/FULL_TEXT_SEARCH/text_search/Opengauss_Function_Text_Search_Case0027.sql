--  @testpoint:停用词测试
--停用词影响tsvector中的位置
SELECT to_tsvector('english','in the list of stop words');
SELECT to_tsvector('english','list stop words');
--包含和不包含停用词的文档计算出的排序是完全不同的
SELECT ts_rank_cd (to_tsvector('english','in the list of stop words'), to_tsquery('list & stop'));
SELECT ts_rank_cd (to_tsvector('english','list stop words'), to_tsquery('list & stop'));