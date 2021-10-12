--  @testpoint:重置文本搜索配置属性语法测试
--创建文本搜索配置
DROP TEXT SEARCH CONFIGURATION if exists ngram2;
CREATE TEXT SEARCH CONFIGURATION ngram2 (parser=ngram) WITH (gram_size = 2, grapsymbol_ignore = false);
--增加映射
ALTER TEXT SEARCH CONFIGURATION ngram2 ADD MAPPING FOR numeric WITH simple,english_stem;
--重置文本搜索配置属性，配置选项不存在
ALTER TEXT SEARCH CONFIGURATION ngram2 reset (gram_size,grapsymbol_ignore,punctuation_ignore);
--查询配置信息，分词相关配置选项有值
select cfgname,cfoptions from pg_ts_config where cfgname='ngram2';
--删除文本搜索配置
DROP TEXT SEARCH CONFIGURATION ngram2;