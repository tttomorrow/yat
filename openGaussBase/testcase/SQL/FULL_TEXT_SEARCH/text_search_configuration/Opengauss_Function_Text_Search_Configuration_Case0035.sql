--  @testpoint:ALTER TEXT SEARCH CONFIGURATION，用户权限测试（sysdmin用户）
--预置条件：当前用户为sysadmin用户
--创建文本搜索配置
drop TEXT SEARCH CONFIGURATION if exists ngram2;
CREATE TEXT SEARCH CONFIGURATION ngram2 (parser=ngram) WITH (gram_size = 2, grapsymbol_ignore = false);
--创建词典
DROP TEXT SEARCH DICTIONARY IF EXISTS pg_dict;
CREATE TEXT SEARCH DICTIONARY pg_dict (TEMPLATE = Simple);
--增加文本搜索配置字串类型映射（有权限）
ALTER TEXT SEARCH CONFIGURATION ngram2  ADD MAPPING FOR grapsymbol with pg_dict ;
--删除文本搜索配置
drop TEXT SEARCH CONFIGURATION ngram2 cascade;
--删除词典
DROP TEXT SEARCH DICTIONARY pg_dict cascade;
