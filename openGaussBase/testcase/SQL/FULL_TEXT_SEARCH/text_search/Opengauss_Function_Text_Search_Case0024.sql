--  @testpoint:函数ts_lexize测试，单一token
--查看文本搜索字典记录
select dictname,dictinitoption from PG_TS_DICT;
--函数ts_lexize用于进行词典测试，指定字典名为simple
SELECT ts_lexize('simple', 'stars');
--指定字典名为english_stem
SELECT ts_lexize('english_stem', 'stars');
--指定字典名为english_stem，token为停用词
SELECT ts_lexize('english_stem', 'a');
--指定字典名为english_stem，token为空字符串
SELECT ts_lexize('english_stem', '');

