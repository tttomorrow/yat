--  @testpoint:创建simple词典,指定停用词表文件全名
drop TEXT SEARCH DICTIONARY if exists public.simple_dict;
--停用词表文件全名为english.stop，合理报错
CREATE TEXT SEARCH DICTIONARY public.simple_dict (
     TEMPLATE = pg_catalog.simple,
     STOPWORDS = english.stop
);
--清理环境：no need to clean
