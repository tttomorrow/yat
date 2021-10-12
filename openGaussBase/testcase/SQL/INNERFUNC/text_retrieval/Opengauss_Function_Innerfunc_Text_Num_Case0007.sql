-- @testpoint: 文本检索函数numnode()与to_tsquery结合使用

drop table if exists ts_zhparser;
create table ts_zhparser(id int, body text);
insert into ts_zhparser values(2, 'fat:ab & cats');
select numnode(to_tsquery(body)) from ts_zhparser;

--清理环境
drop table if exists ts_zhparser;