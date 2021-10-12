--  @testpoint:ngram类型解析器，配置参数无效性测试
--创建文本搜索配置,gram_size取负整数，合理报错
DROP TEXT SEARCH CONFIGURATION if exists ngram2;
CREATE TEXT SEARCH CONFIGURATION ngram2 (parser=ngram) WITH (gram_size = -2, punctuation_ignore= true,grapsymbol_ignore = false);
--创建文本搜索配置,gram_size取0，合理报错
DROP TEXT SEARCH CONFIGURATION if exists ngram3;
CREATE TEXT SEARCH CONFIGURATION ngram3 (parser=ngram) WITH (gram_size = 0, punctuation_ignore= true,grapsymbol_ignore = false);
--创建文本搜索配置,gram_size取5，合理报错
DROP TEXT SEARCH CONFIGURATION if exists ngram4;
CREATE TEXT SEARCH CONFIGURATION ngram4 (parser=ngram) WITH (gram_size = 5, punctuation_ignore= true,grapsymbol_ignore = false);
--创建文本搜索配置,gram_size取值为非数字，合理报错
DROP TEXT SEARCH CONFIGURATION if exists ngram5;
CREATE TEXT SEARCH CONFIGURATION ngram5 (parser=ngram) WITH (gram_size = 2*, punctuation_ignore= true,grapsymbol_ignore = false);