--  @testpoint:修改文本搜索配置的schema
--默认public模式下创建文本搜索配置
DROP TEXT SEARCH CONFIGURATION if exists ngram2;
CREATE TEXT SEARCH CONFIGURATION ngram2 (parser=ngram) WITH (gram_size = 2, grapsymbol_ignore = false);
--查询schema
drop schema if exists test_schema1;
select schema_name from information_schema.schemata where schema_name = 'test_schema1';
--修改文本搜索配置的schema(schema不存在),合理报错
ALTER TEXT SEARCH CONFIGURATION ngram2 SET SCHEMA test_schema1;
--删除文本搜索配置
DROP TEXT SEARCH CONFIGURATION ngram2;