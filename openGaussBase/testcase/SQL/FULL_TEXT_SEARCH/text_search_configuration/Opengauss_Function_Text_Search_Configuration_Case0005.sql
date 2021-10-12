--  @testpoint:ngram类型解析器,添加对应的配置参数
---创建文本搜索配置,ngram类型解析器对应的配置参数均取默认值
DROP TEXT SEARCH CONFIGURATION if exists ngram2;
CREATE TEXT SEARCH CONFIGURATION ngram2 (parser=ngram) WITH (gram_size = 2, punctuation_ignore= true,grapsymbol_ignore = false);
--创建文本搜索配置,ngram类型解析器对应的配置参数取其他值
DROP TEXT SEARCH CONFIGURATION if exists ngram3;
CREATE TEXT SEARCH CONFIGURATION ngram3 (parser=ngram) WITH (gram_size = 2, punctuation_ignore= false,grapsymbol_ignore = true);
--创建文本搜索配置,gram_size取1
DROP TEXT SEARCH CONFIGURATION if exists ngram4;
CREATE TEXT SEARCH CONFIGURATION ngram4 (parser=ngram) WITH (gram_size = 1, punctuation_ignore= false,grapsymbol_ignore = true);
--创建文本搜索配置,gram_size取4
DROP TEXT SEARCH CONFIGURATION if exists ngram5;
CREATE TEXT SEARCH CONFIGURATION ngram5 (parser=ngram) WITH (gram_size = 4, punctuation_ignore= false,grapsymbol_ignore = true);
--删除文本搜索配置
DROP TEXT SEARCH CONFIGURATION ngram2;
DROP TEXT SEARCH CONFIGURATION ngram3;
DROP TEXT SEARCH CONFIGURATION ngram4;
DROP TEXT SEARCH CONFIGURATION ngram5;




