--  @testpoint:ts_token_type函数测试
--testpoint1:获取default分析器的记号类型（23种）
 SELECT ts_token_type('default');
--testpoint2:获取ngram分析器的记号类型（6种）
  SELECT ts_token_type('ngram');
--testpoint3:获取pound分析器的记号类型（6种）
  SELECT ts_token_type('pound');
--清理环境 no need to clean
