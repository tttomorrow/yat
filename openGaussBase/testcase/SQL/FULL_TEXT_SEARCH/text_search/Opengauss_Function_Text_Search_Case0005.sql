--  @testpoint:plainto_tsquery函数测试
--文本被解析并且标准化，然后在存在的词之间插入&(AND)布尔运算符
SELECT plainto_tsquery('english', 'The Fat Rats');
--不加分词器
SELECT plainto_tsquery('The Fat Rats');
--检索条件中添加布尔运算符（不识别运算符）
SELECT plainto_tsquery('english', 'The Fat & Rats');
SELECT plainto_tsquery('The Fat & Rats');
--检索条件中添加权重（不识别权重标签），
SELECT plainto_tsquery('english', 'The Fat Rats:AB');
SELECT plainto_tsquery('The Fat:D Rats');
--检索条件中添加前缀（不识别前缀，作为符号丢弃）
SELECT plainto_tsquery('The Fat:*A Rats');


