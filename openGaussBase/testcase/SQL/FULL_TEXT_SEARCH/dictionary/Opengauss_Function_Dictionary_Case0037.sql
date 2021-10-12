--  @testpoint:修改词典定义语法测试
--创建simple词典
drop TEXT SEARCH DICTIONARY if exists public.simple_dict cascade;
CREATE TEXT SEARCH DICTIONARY public.simple_dict (
     TEMPLATE = pg_catalog.simple,
     STOPWORDS = english,
     ACCEPT = false
);
--使用alter语句修改词典option参数值，添加等号（=）和value
ALTER TEXT SEARCH DICTIONARY public.simple_dict (
     STOPWORDS = german,
     ACCEPT = true
);
--删除词典
drop TEXT SEARCH DICTIONARY public.simple_dict cascade;