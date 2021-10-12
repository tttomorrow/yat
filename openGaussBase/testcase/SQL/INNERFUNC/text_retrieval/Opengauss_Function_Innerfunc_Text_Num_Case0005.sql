-- @testpoint: 文本检索函数numnode()不使用逻辑运算

drop table if exists ts_zhparser;
create table ts_zhparser(id int, body text);
insert into ts_zhparser values(2, 'fat');
select numnode(body :: tsquery) from ts_zhparser;

--清理环境
drop table if exists ts_zhparser;