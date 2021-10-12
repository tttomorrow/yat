--  @testpoint:重命名文本搜索配置名称语法测试
--创建文本搜索配置
DROP TEXT SEARCH CONFIGURATION if exists ngram2;
CREATE TEXT SEARCH CONFIGURATION ngram2 (parser=ngram) WITH (gram_size = 2, grapsymbol_ignore = false);
--重命名文本搜索配置名称
DROP TEXT SEARCH CONFIGURATION if exists new_ngram2;
ALTER TEXT SEARCH CONFIGURATION ngram2 RENAME TO new_ngram2;
--使用新名称查询文本搜索配置
SELECT cfgname,cfoptions from pg_ts_config where cfgname='new_ngram2';
--删除文本搜索配置
DROP TEXT SEARCH CONFIGURATION new_ngram2;