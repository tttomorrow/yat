--  @testpoint:创建simple词典，设置参数accept为false，使用词典
--创建simple词典
DROP TEXT SEARCH DICTIONARY if exists public.simple_dict;
CREATE TEXT SEARCH DICTIONARY public.simple_dict (TEMPLATE = simple, Accept = false );
--使用词典，返回null
SELECT ts_lexize('public.simple_dict','Yes');
SELECT ts_lexize('public.simple_dict','The');
--删除词典
DROP TEXT SEARCH DICTIONARY public.simple_dict;