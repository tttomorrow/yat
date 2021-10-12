-- @testpoint: 文本检索函数numnode()返回tsquery类型的单词加上操作符的数量

drop table if exists ts_zhparser;
create table ts_zhparser(id int, body text);
insert into ts_zhparser values(2, '(fat & rat) | cat');
select numnode(plainto_tsquery('english',body)) from ts_zhparser;

--清理环境
drop table if exists ts_zhparser;