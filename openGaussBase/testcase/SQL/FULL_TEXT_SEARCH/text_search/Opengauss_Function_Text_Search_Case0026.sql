--  @testpoint:函数ts_lexize测试，多个token(资料表示ts_lexize函数支持单一token，不支持文本，待确认)
--查看文本搜索字典记录
select dictname,dictinitoption from PG_TS_DICT;
--函数ts_lexize用于进行词典测试，指定字典名为simple
SELECT ts_lexize('simple', 'many stars in the sky');
--指定字典名为english_stem，token为停用词
SELECT ts_lexize('english_stem', 'a the fats');
