--  @testpoint:创建词典，指定STOPWORDS后缀为stops，合理报错
--创建字典，模板名为simple
DROP TEXT SEARCH DICTIONARY IF EXISTS public.simple_dict;
CREATE TEXT SEARCH DICTIONARY public.simple_dict (
     TEMPLATE = pg_catalog.simple,
     STOPWORDS = english.stops
);
--清理环境:no need to clean