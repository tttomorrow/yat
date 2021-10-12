--  @testpoint:创建simple词典，并测试词典的大小写，以及停用词
--创建词典
drop TEXT SEARCH DICTIONARY if exists public.simple_dict cascade;
CREATE TEXT SEARCH DICTIONARY public.simple_dict (
     TEMPLATE = pg_catalog.simple,
     STOPWORDS = english
);
--使用词典，测试大小写，大写字母转小写
SELECT ts_lexize('public.simple_dict','HELLO');
--大写转小写，单词结尾es不删除
SELECT ts_lexize('public.simple_dict','toMAtoes');
--停用词和非停用词混合，原样输出
SELECT ts_lexize('public.simple_dict','a cat the dog');
--只有一个字符且为停用词，返回空数组
SELECT ts_lexize('public.simple_dict','the');
--修改词典参数，参数ACCEPT=false，即不识别非停用词
ALTER TEXT SEARCH DICTIONARY public.simple_dict ( Accept = false );
--测试词典，不识别非停用词，返回null
SELECT ts_lexize('public.simple_dict','HELLO');
--只有一个字符且为停用词，识别停用词，返回空数组
SELECT ts_lexize('public.simple_dict','the');
--停用词和非停用词混合，返回null
SELECT ts_lexize('public.simple_dict','a cat the dog');
--字串为空字符，返回null
SELECT ts_lexize('public.simple_dict',' ');
--字串包含空格,返回null
SELECT ts_lexize('public.simple_dict','a  dog   ');
--删除词典
drop TEXT SEARCH DICTIONARY public.simple_dict cascade;