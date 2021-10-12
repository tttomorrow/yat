-- @testpoint: 文本检索函数strip()处理含有位置常量的tsvector类型

drop table if exists ts_zhparser;
create table ts_zhparser(id int, body text);
insert into ts_zhparser values(2, 'a:1 fat:2');
select strip(body :: tsvector) from ts_zhparser;

--清理环境
drop table if exists ts_zhparser;