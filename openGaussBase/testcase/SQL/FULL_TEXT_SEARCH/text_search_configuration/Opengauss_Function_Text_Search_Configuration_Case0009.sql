--  @testpoint:增加文本搜索配置字串类型映射语法测试
--创建文本搜索配置
DROP TEXT SEARCH CONFIGURATION if exists ngram2;
CREATE TEXT SEARCH CONFIGURATION ngram2 (parser=ngram);
--创建simple字典
DROP TEXT SEARCH DICTIONARY IF EXISTS pg_dict;
CREATE TEXT SEARCH DICTIONARY pg_dict (TEMPLATE = Simple);
--增加文本搜索配置字串类型映射语法（文本搜索配置和解析器的token类型对应）
ALTER TEXT SEARCH CONFIGURATION ngram2 ADD MAPPING FOR zh_words WITH simple,english_stem;
ALTER TEXT SEARCH CONFIGURATION ngram2 ADD MAPPING FOR numeric WITH english_stem, french_stem;
--查询文本搜索配置相关信息
SELECT cfgname,cfoptions  FROM PG_TS_CONFIG where cfgname='ngram2';
--删除文本搜索配置
DROP TEXT SEARCH CONFIGURATION ngram2;
--删除词典
DROP TEXT SEARCH DICTIONARY pg_dict;

