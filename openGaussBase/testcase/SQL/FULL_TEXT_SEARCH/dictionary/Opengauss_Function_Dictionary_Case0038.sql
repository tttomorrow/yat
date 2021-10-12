--  @testpoint:修改词典的TEMPLATE参数值,合理报错
--创建simple词典
drop TEXT SEARCH DICTIONARY if exists public.simple_dict cascade;
CREATE TEXT SEARCH DICTIONARY public.simple_dict (
     TEMPLATE = pg_catalog.simple,
     STOPWORDS = english,
     ACCEPT = false
);
--使用alter语句修改词典模板，合理报错
ALTER TEXT SEARCH DICTIONARY public.simple_dict (
     TEMPLATE = pg_catalog.Synonym
);
--删除词典
drop TEXT SEARCH DICTIONARY public.simple_dict cascade;