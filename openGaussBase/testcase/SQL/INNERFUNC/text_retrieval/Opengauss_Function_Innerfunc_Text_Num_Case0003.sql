-- @testpoint: 文本检索函数numnode()与plainto_tsquery结合使用，分词器默认不填

drop table if exists ts_zhparser;
create table ts_zhparser(id int, body text);
insert into ts_zhparser values(2, 'the fat');
select numnode(plainto_tsquery(body)) from ts_zhparser;

--清理环境
drop table if exists ts_zhparser;