-- @testpoint: 文本检索函数setweight给本身有权值的tsvector类型的元素分配权值

drop table if exists ts_zhparser;
create table ts_zhparser(id int, body text);
insert into ts_zhparser values(2, 'a:1b fat:2');
select setweight(body :: tsvector, 'a') from ts_zhparser;

--清理环境
drop table if exists ts_zhparser;