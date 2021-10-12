--  @testpoint:创建文本搜索配置语法,PARSER参数测试（无效性测试）
--指定解析器为ngrams,合理报错
DROP TEXT SEARCH CONFIGURATION if exists ngram2;
CREATE TEXT SEARCH CONFIGURATION ngram2 (parser=ngrams);
--指定解析器为defaults,合理报错
DROP TEXT SEARCH CONFIGURATION if exists default2;
CREATE TEXT SEARCH CONFIGURATION default2 (parser=defaults);
