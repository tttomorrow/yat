-- @testpoint: 文本检索函数plainto_tsquery分词器参数缺省

drop table if exists ts_zhparser;
create table ts_zhparser(id int, body text);
insert into ts_zhparser values(2, 'the fat rats,');
select plainto_tsquery(body) from ts_zhparser;

--清理环境
drop table if exists ts_zhparser;