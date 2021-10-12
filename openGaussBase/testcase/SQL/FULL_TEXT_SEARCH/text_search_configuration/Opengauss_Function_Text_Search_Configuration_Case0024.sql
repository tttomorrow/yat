--  @testpoint:修改文本搜索配置的schema
--默认public模式下创建文本搜索配置
DROP TEXT SEARCH CONFIGURATION if exists ngram2;
CREATE TEXT SEARCH CONFIGURATION ngram2 (parser=ngram) WITH (gram_size = 2, grapsymbol_ignore = false);
--创建schema
drop schema if exists test_schema;
create schema test_schema;
--修改文本搜索配置的schema(schema存在)
ALTER TEXT SEARCH CONFIGURATION ngram2 SET SCHEMA test_schema;
--删除文本搜索配置
DROP TEXT SEARCH CONFIGURATION test_schema.ngram2;
--删除schema
drop schema test_schema;