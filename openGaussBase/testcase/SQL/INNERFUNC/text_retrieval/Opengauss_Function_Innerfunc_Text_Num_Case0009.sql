-- @testpoint: 文本检索函数numnode()，tsquery类型为一个空字符

drop table if exists ts_zhparser;
create table ts_zhparser(id int, body text);
insert into ts_zhparser values(2, '');
select numnode(body :: tsquery) from ts_zhparser;

--清理环境
drop table if exists ts_zhparser;