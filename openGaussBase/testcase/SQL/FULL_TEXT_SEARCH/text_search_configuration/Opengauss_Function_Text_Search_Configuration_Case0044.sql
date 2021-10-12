--  @testpoint:创建文本搜索配置，ngram类型解析器配置参数有误，合理报错
--创建文本搜索配置ngram_test，gram_size参数有误，合理报错
drop TEXT SEARCH CONFIGURATION if exists ngram_test;
CREATE TEXT SEARCH CONFIGURATION ngram_test (PARSER = ngram) with (gram_sizes = 2);
--punctuation_ignore参数有误，合理报错
CREATE TEXT SEARCH CONFIGURATION ngram_test1 (PARSER = ngram) with (punctuation_ignores = false);
--grapsymbol_ignore参数有误，合理报错
CREATE TEXT SEARCH CONFIGURATION ngram_test2 (PARSER = ngram) with (grapsymbol_ignores = false);
