-- @testpoint: 文本检索函数setweight与to_tsvector结合使用

drop table if exists ts_zhparser;
create table ts_zhparser(id int, body text);
insert into ts_zhparser values(2, 'fat fet');
select setweight(to_tsvector(body), 'a') from ts_zhparser;

--清理环境
drop table if exists ts_zhparser;