--  @testpoint:创建文本搜索配置，文本搜索分析器的名称指定为pound
drop TEXT SEARCH CONFIGURATION if exists pound_test cascade;
CREATE TEXT SEARCH CONFIGURATION pound_test (PARSER = pound);
--添加类型映射
ALTER TEXT SEARCH CONFIGURATION pound_test ADD MAPPING FOR multisymbol WITH simple;
--再次创建文本搜索配置，使用copy复制现有文本搜索配置pound_test
drop TEXT SEARCH CONFIGURATION if exists pound_test1 cascade;
CREATE TEXT SEARCH CONFIGURATION pound_test1 (copy = pound_test);
--查询文本搜索配置信息
select cfgname,cfgname,cfgparser from PG_TS_CONFIG where cfgname='pound_test';
select cfgname,cfgname,cfgparser from PG_TS_CONFIG where cfgname ='pound_test1';
--删除文本搜索配置
drop TEXT SEARCH CONFIGURATION pound_test cascade;
drop TEXT SEARCH CONFIGURATION pound_test1 cascade;