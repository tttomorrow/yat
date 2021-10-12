--- Case Type： Comment
--- Case Name： 在文本搜索配置上添加注释

--创建文本搜索配置
create text search configuration ngram2 (parser=ngram) with (gram_size = 2, grapsymbol_ignore = false);

--给文本搜索配置添加注释信息
comment on text search configuration ngram2 is '测试文本搜索配置注释添加成功';

--在相关系统表中查看注释是否添加成功
select description from pg_description where objoid=(select oid from pg_ts_config where cfgname='ngram2');

--清理环境
drop text search configuration ngram2;

