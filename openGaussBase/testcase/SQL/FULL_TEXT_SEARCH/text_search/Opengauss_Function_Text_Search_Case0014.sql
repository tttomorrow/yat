--  @testpoint:tsquery类型的查询，相关函数测试
--numnode(tsquery)
--返回0，只包含停用词
SELECT numnode(plainto_tsquery('the any'));
--返回大于0
SELECT numnode('foo & bar | dog'::tsquery);
SELECT numnode('foo & bar | 中文'::tsquery);
SELECT numnode($$foo & bar | '   '$$::tsquery);
SELECT numnode($$'   '$$::tsquery);
--querytree(query tsquery)
SELECT querytree('foo & ! bar'::tsquery);
SELECT querytree('! bar'::tsquery);