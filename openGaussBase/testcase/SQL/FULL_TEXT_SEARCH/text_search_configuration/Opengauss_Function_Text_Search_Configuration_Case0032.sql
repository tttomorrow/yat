--  @testpoint:增加文本搜索配置字串类型映射语法,多个词典名测试
--创建文本搜索配置
DROP TEXT SEARCH CONFIGURATION if exists english2;
CREATE TEXT SEARCH CONFIGURATION english2 (parser=default);
--创建simple字典
DROP TEXT SEARCH DICTIONARY IF EXISTS pg_dict;
CREATE TEXT SEARCH DICTIONARY pg_dict (TEMPLATE = Simple);
--再创建一个词典
DROP TEXT SEARCH DICTIONARY IF EXISTS pg_dict1;
CREATE TEXT SEARCH DICTIONARY pg_dict1 (TEMPLATE = Simple);
--增加文本搜索配置字串类型映射
ALTER TEXT SEARCH CONFIGURATION english2 ADD MAPPING FOR url WITH  pg_dict,pg_dict1;
--查询配置信息
select cfgname,cfoptions from PG_TS_CONFIG where cfgname='english2';
--删除文本搜索配置
DROP TEXT SEARCH CONFIGURATION english2;
--删除词典
DROP TEXT SEARCH DICTIONARY pg_dict;
DROP TEXT SEARCH DICTIONARY pg_dict1;