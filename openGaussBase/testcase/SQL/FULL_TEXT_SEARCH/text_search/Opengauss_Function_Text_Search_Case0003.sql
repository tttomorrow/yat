--  @testpoint:to_tsquery函数测试
--指定分词器
SELECT to_tsquery('english', 'The & Fat & Rats');
--不指定分词器
SELECT to_tsquery('The & Fat & Rats');
--检索条件由布尔运算符|组成
SELECT to_tsquery('english', 'The | Fat | Rats');
--检索条件包含&和 !运算符
SELECT to_tsquery('fat & rat & ! cat');
--检索条件，附加权重
SELECT to_tsquery('english', 'Fat | Rats:AB');
--指定*，匹配前缀
SELECT to_tsquery('supern:*A & star:A*B');
--权重D,输出含有D
SELECT to_tsquery('supern:*D & star:A*B');
--权重以小写字母表示（输出为大写）
SELECT to_tsquery('supern:*d & star:a*b');
