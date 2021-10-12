-- @testpoint: 文本检索函数plainto_tsquery，参数不是文本类型

drop table if exists ts_zhparser;
create table ts_zhparser(id int, body text);
insert into ts_zhparser values(2, 'the fat rats & ear');
select plainto_tsquery(id) from ts_zhparser;

--清理环境
drop table if exists ts_zhparser;