--  @testpoint:opengauss关键字parser(非保留)，创建 ,修改，删除文本搜索配置

DROP TEXT SEARCH CONFIGURATION  if exists ngram2;

CREATE TEXT SEARCH CONFIGURATION ngram2 (parser=ngram) WITH (gram_size = 2, grapsymbol_ignore = false);

ALTER TEXT SEARCH CONFIGURATION ngram2 ADD MAPPING FOR multisymbol WITH simple;

DROP TEXT SEARCH CONFIGURATION  ngram2;



