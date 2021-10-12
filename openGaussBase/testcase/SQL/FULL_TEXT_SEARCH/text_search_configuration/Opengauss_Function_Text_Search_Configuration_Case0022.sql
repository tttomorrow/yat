--  @testpoint:修改文本搜索配置的所有者语法测试
--创建文本搜索配置
DROP TEXT SEARCH CONFIGURATION if exists ngram2;
CREATE TEXT SEARCH CONFIGURATION ngram2 (parser=ngram) WITH (gram_size = 2, grapsymbol_ignore = false);
--查询用户是否存在
drop user if exists lika;
select usename from pg_user where usename='lika';
--修改所有者(用户不存在)，合理报错
ALTER TEXT SEARCH CONFIGURATION ngram2 owner to lika;
--删除文本搜索配置
DROP TEXT SEARCH CONFIGURATION ngram2;
