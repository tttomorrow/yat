--  @testpoint:修改文本搜索配置属性语法测试
--创建文本搜索配置
DROP TEXT SEARCH CONFIGURATION if exists ngram2;
CREATE TEXT SEARCH CONFIGURATION ngram2 (parser=ngram) WITH (gram_size = 2, grapsymbol_ignore = false);
--修改文本搜索配置参数值,参数不加括号，合理报错
ALTER TEXT SEARCH CONFIGURATION ngram2 SET gram_size = 3,grapsymbol_ignore = true;
--删除文本搜索配置
DROP TEXT SEARCH CONFIGURATION ngram2;