--  @testpoint:创建文本搜索配置语法,PARSER参数测试（合理性测试）
--指定解析器为ngram
DROP TEXT SEARCH CONFIGURATION if exists ngram2;
CREATE TEXT SEARCH CONFIGURATION ngram2 (parser=ngram);
--指定解析器为default
DROP TEXT SEARCH CONFIGURATION if exists default2;
CREATE TEXT SEARCH CONFIGURATION default2 (parser=default);
--指定解析器为pound
DROP TEXT SEARCH CONFIGURATION if exists pound2;
CREATE TEXT SEARCH CONFIGURATION pound2 (parser=pound);
--删除文本搜索配置
DROP TEXT SEARCH CONFIGURATION ngram2;
DROP TEXT SEARCH CONFIGURATION default2;
DROP TEXT SEARCH CONFIGURATION pound2;
