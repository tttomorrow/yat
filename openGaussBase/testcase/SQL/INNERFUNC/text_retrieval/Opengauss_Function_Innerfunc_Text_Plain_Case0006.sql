-- @testpoint: 文本检索函数plainto_tsquery，参数为null

drop table if exists ts_zhparser;
create table ts_zhparser(id int, body text);
insert into ts_zhparser (id) values (3);
select plainto_tsquery(body) from ts_zhparser;

--清理环境
drop table if exists ts_zhparser;