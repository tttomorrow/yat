-- @testpoint: 文本检索函数numnode()参数为一不存在的列 合理报错

drop table if exists ts_zhparser;
create table ts_zhparser(id int, body text);
insert into ts_zhparser values(2, 'fat');
select numnode(bodyy :: tsquery) from ts_zhparser;

--清理环境
drop table if exists ts_zhparser;