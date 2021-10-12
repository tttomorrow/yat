--  @testpoint:删除存在的文本搜索配置，添加级联删除选项
--创建schema
drop schema if exists test_schema;
create schema test_schema;
--创建文本搜索配置
drop TEXT SEARCH CONFIGURATION if exists test_schema.ngram2;
CREATE TEXT SEARCH CONFIGURATION  test_schema.ngram2 (parser=ngram) WITH (gram_size = 2, grapsymbol_ignore = false);
--删除文本搜索配置
drop TEXT SEARCH CONFIGURATION test_schema.ngram2 RESTRICT;
--创建文本搜索配置
drop TEXT SEARCH CONFIGURATION if exists test_schema.ngram2;
CREATE TEXT SEARCH CONFIGURATION  test_schema.ngram2 (parser=ngram) WITH (gram_size = 2, grapsymbol_ignore = false);
--删除文本搜索配置
drop TEXT SEARCH CONFIGURATION test_schema.ngram2 cascade;
--删除schema
drop schema test_schema;