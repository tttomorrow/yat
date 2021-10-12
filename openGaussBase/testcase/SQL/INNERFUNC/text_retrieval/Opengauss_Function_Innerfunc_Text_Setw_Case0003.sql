-- @testpoint: 文本检索函数setweight入参权值为非字符型、空值，非字符型时合理报错

drop table if exists ts_zhparser;
create table ts_zhparser(id int, body text);
insert into ts_zhparser values(2, 'a:1 fat:2');
select setweight('fat:2,4 cat:3 rat:5b'::tsvector, 1);
select setweight('fat:2,4 cat:3 rat:5b'::tsvector, '');

--清理环境
drop table if exists ts_zhparser;