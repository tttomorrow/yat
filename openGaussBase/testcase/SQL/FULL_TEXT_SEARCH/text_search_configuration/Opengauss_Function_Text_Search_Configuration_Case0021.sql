--  @testpoint:修改文本搜索配置的所有者语法测试
--创建文本搜索配置
DROP TEXT SEARCH CONFIGURATION if exists ngram2;
CREATE TEXT SEARCH CONFIGURATION ngram2 (parser=ngram) WITH (gram_size = 2, grapsymbol_ignore = false);
--创建用户
DROP user if exists joe;
CREATE USER joe IDENTIFIED BY 'Bigdata@123';
--修改所有者(用户存在)
ALTER TEXT SEARCH CONFIGURATION ngram2 owner to joe;
--删除文本搜索配置
DROP TEXT SEARCH CONFIGURATION ngram2;
--删除用户
drop user joe;