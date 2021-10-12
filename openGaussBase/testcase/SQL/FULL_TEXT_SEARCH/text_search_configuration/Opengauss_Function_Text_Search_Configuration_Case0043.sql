-- @testpoint: 创建文本搜索配置，解析器非default、ngram，解析器为zhparser时，合理报错
--创建文本搜索配置copypg_catalog.pound
drop TEXT SEARCH CONFIGURATION if exists pound2;
CREATE TEXT SEARCH CONFIGURATION pound2 (COPY = pg_catalog.pound);
--查看文本搜索配置文件信息
select cfgname,cfoptions from PG_TS_CONFIG where cfgname='pound2';
--创建文本搜索配置parser_name为zhparser，合理报错
drop TEXT SEARCH CONFIGURATION if exists zhparser_test;
CREATE TEXT SEARCH CONFIGURATION zhparser_test (PARSER = zhparser);
--删除文本搜索配置
drop TEXT SEARCH CONFIGURATION  pound2;
