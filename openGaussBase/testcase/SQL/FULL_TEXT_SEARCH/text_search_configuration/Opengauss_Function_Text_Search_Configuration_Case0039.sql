--  @testpoint:删除不存在的文本搜索配置
--检查文本搜索配置信息,不存在名字为ngram3的搜索配置
select cfgname from PG_TS_CONFIG where cfgname='ngram3';
--删除，添加if exists选项，发出notice
drop TEXT SEARCH CONFIGURATION if exists ngram3;
--删除，省略if exists选项，合理报错
drop TEXT SEARCH CONFIGURATION ngram3;