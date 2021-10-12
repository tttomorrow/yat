--  @testpoint:tsvector查询，相关函数测试
--给tsvector类型的每个元素分配无效权值，报错
SELECT setweight('fat:2,4 cat:3 rat:5B'::tsvector, 'E');
--tsquery类型，报错
SELECT length('fat & cat'::tsquery);