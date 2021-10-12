--  @testpoint:更改文本搜索配置字典语法测试，文本搜索字典名称不存在
--创建文本搜索配置
DROP TEXT SEARCH CONFIGURATION if exists english2;
CREATE TEXT SEARCH CONFIGURATION english2 (parser=default);
--创建simple字典
DROP TEXT SEARCH DICTIONARY IF EXISTS pg_dict;
CREATE TEXT SEARCH DICTIONARY pg_dict (TEMPLATE = Simple);
--增加文本搜索配置字串类型映射
ALTER TEXT SEARCH CONFIGURATION english2 ADD MAPPING FOR numword WITH simple,dutch_stem;
--更改文本搜索配置字典类型为germans_stem，合理报错
ALTER TEXT SEARCH CONFIGURATION english2 ALTER MAPPING REPLACE dutch_stem with germans_stem;
--删除文本搜索配置
DROP TEXT SEARCH CONFIGURATION english2;
--删除字典
DROP TEXT SEARCH DICTIONARY pg_dict;
