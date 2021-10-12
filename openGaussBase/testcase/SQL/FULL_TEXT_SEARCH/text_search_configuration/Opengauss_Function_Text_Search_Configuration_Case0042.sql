--  @testpoint:创建文本搜索配置PARSER和COPY选项同时出现，合理报错
--创建文本搜索配置
drop TEXT SEARCH CONFIGURATION if exists ngram2;
CREATE TEXT SEARCH CONFIGURATION ngram2 (parser = ngram，COPY = pg_catalog.ngram) WITH (gram_size = 2, grapsymbol_ignore = false);