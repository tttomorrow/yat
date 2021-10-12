--  @testpoint:修改文本搜索配置属性语法测试
--创建文本搜索配置
DROP TEXT SEARCH CONFIGURATION if exists ngram2;
CREATE TEXT SEARCH CONFIGURATION ngram2 (parser=ngram) WITH (gram_size = 2, grapsymbol_ignore = false);
--增加映射
ALTER TEXT SEARCH CONFIGURATION ngram2 ADD MAPPING FOR numeric WITH simple,english_stem;
--修改文本搜索配置参数值,参数值在创建时未添加
ALTER TEXT SEARCH CONFIGURATION ngram2 SET (gram_size = 3,grapsymbol_ignore = true,punctuation_ignore = false);
--查询文本搜索配置记录
SELECT cfgname,cfoptions  FROM PG_TS_CONFIG where cfgname='ngram2';
--删除文本搜索配置
DROP TEXT SEARCH CONFIGURATION ngram2;