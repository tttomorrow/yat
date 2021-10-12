-- @testpoint: 文本检索numnode()函数，返回tsquery类型单词数量

drop table if exists ts_zhparser;
create table ts_zhparser(id int, body text);
insert into ts_zhparser values(2, 'fat & (rat | cat)');
select numnode(body :: tsquery) from ts_zhparser;

--清理环境
drop table if exists ts_zhparser;