--  @testpoint:tsvector查询，相关函数测试
--连接两个tsvector类型的词汇（tsvector || tsvector）
SELECT 'a:1 b:2'::tsvector || 'c:1 d:2 b:3'::tsvector AS RESULT;
--给tsvector类型的每个元素分配权值（setweight）
SELECT setweight('fat:2,4 cat:3 rat:5B'::tsvector, 'A');
--给tsvector类型的每个元素分配权值D，输出结果没有D
SELECT setweight('fat:2,4 cat:3 rat:5B'::tsvector, 'D');
--tsvector类型中含有中文
SELECT setweight('中文:2,4 cat:3 rat:5B'::tsvector, 'A');
--只给权重，不给位置信息，返回结果没有权重
SELECT setweight('fat cat rat'::tsvector, 'AB');
--tsvector类型词汇的单词数（length）
SELECT length('fat:2,4 cat:3 rat:5A'::tsvector);
--删除tsvector类型单词中的position和权值
SELECT strip('fat:2,4 cat:3 rat:5A'::tsvector);

