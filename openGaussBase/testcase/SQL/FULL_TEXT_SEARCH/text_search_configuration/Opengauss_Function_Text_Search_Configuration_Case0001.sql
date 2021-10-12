--  @testpoint:创建文本搜索配置语法，name参数测试
--创建文本搜索配置不带模式
DROP TEXT SEARCH CONFIGURATION if exists ngram2;
CREATE TEXT SEARCH CONFIGURATION ngram2 (parser=ngram);
--创建模式
drop schema if exists test_schema;
create schema test_schema;
--创建文本搜索配置带模式
DROP TEXT SEARCH CONFIGURATION if exists test_schema.ngram2;
CREATE TEXT SEARCH CONFIGURATION test_schema.ngram2 (parser=ngram);
--删除文本搜索配置
DROP TEXT SEARCH CONFIGURATION ngram2;
DROP TEXT SEARCH CONFIGURATION test_schema.ngram2;
--删除模式
drop schema test_schema;