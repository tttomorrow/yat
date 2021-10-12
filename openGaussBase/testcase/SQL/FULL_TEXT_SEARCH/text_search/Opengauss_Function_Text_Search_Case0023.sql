--  @testpoint:函数ts_token_type测试，通过parser_oid 获取分析器定义的记号类型
--查看default解析器的oid
select oid from PG_TS_PARSER where prsname = 'default';
SELECT ts_token_type(3722);
SELECT * from ts_token_type(3722);
--查看ngram解析器的oid
select oid from PG_TS_PARSER where prsname = 'ngram';
SELECT ts_token_type(3789);
SELECT * from ts_token_type(3789);
--查看pound解析器的oid
select oid from PG_TS_PARSER where prsname = 'pound';
SELECT ts_token_type(3801);
SELECT * from ts_token_type(3801);

