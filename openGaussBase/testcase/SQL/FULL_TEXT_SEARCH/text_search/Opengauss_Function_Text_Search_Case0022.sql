--  @testpoint:函数ts_token_type测试
--返回指定解析器default的token类型及其描述信息
SELECT * FROM ts_token_type('default');
SELECT ts_token_type('default');
--返回指定解析器ngram的token类型及其描述信息
SELECT * FROM ts_token_type('ngram');
SELECT ts_token_type('ngram');
--回指定解析器pound的token类型及其描述信息
SELECT * FROM ts_token_type('pound');
SELECT ts_token_type('pound');