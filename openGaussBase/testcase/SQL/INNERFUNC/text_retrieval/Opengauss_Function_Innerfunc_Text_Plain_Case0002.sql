-- @testpoint: 文本检索函数numnode()有分词器

drop table if exists ts_zhparser;
create table ts_zhparser(id int, body text);
insert into ts_zhparser values(2, 'the fat rats,');
select plainto_tsquery('english', body) from ts_zhparser;

--清理环境
drop table if exists ts_zhparser;