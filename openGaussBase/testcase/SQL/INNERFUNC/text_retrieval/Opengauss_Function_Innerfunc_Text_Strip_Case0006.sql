-- @testpoint: 文本检索函数strip()处理int类型，合理报错

drop table if exists ts_zhparser;
create table ts_zhparser(id int, body text);
insert into ts_zhparser values(2, 'cat dat');
select strip(id) from ts_zhparser;

--清理环境
drop table if exists ts_zhparser;