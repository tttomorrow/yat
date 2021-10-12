--  @testpoint:函数ts_parse测试
--测试一个解析，ts_parse解析指定的document并返回一系列的记录，一条记录代表一个解析生成的token。每条记录包括标识token类型的tokid，及token文本
SELECT * FROM ts_parse('default', '123 - a number');
SELECT ts_parse('default', 'foo - bar');
--解析器为pound
SELECT * FROM ts_parse('pound', '123 - a number');
--查看default解析器的oid
select oid from PG_TS_PARSER where prsname = 'default';
--ts_parse函数指定parser_oid
SELECT ts_parse(3722, 'foo - bar');
--查看pound解析器的oid
select oid from PG_TS_PARSER where prsname = 'pound';
--ts_parse函数指定parser_oid
SELECT ts_parse(3801, 'foo - bar');
