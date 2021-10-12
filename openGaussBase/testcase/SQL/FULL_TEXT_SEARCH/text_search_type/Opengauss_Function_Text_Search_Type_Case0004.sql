--  @testpoint:文本搜索类型（tsquery无效性测试）
--检索的词汇使用and连接（合理报错）
SELECT 'fat and rat'::tsquery;
--检索的词汇使用and和not连接（合理报错）
SELECT 'fat and rat and not cat'::tsquery;
--检索的词汇使用and和not以及or连接（合理报错）
SELECT 'fat and rat and not cat or dog'::tsquery;