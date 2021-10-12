-- @testpoint: 文本检索函数numnode()，tsquery类型为空

drop table if exists ts_zhparser;
create table ts_zhparser(id int, body text);
insert into ts_zhparser (id) values (3);
select numnode(body :: tsquery) from ts_zhparser;

--清理环境
drop table if exists ts_zhparser;