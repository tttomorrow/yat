--  @testpoint:删除存在的文本搜索配置
--创建文本搜索配置
drop TEXT SEARCH CONFIGURATION if exists ngram2;
CREATE TEXT SEARCH CONFIGURATION ngram2 (parser=ngram) WITH (gram_size = 2, grapsymbol_ignore = false);
--检查文本搜索信息
select cfgname from PG_TS_CONFIG where cfgname='ngram2';
--删除，添加if exists选项，删除成功
drop TEXT SEARCH CONFIGURATION if exists ngram2;
--再次创建文本搜索配置
drop TEXT SEARCH CONFIGURATION if exists ngram3;
CREATE TEXT SEARCH CONFIGURATION ngram3 (parser=ngram) WITH (gram_size = 2, grapsymbol_ignore = false);
--检查文本搜索信息
select cfgname from PG_TS_CONFIG where cfgname='ngram3';
--删除，省略if exists选项，删除成功
drop TEXT SEARCH CONFIGURATION ngram3;