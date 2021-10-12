-- @testpoint: interval时间间隔类型，天数和秒数精度定义不在范围内，提示警告信息

--创建表
drop table if exists interval03;
create table interval03 (name interval day(8) to second(9));

--插入数据
insert into interval03 values ('1234 12:23:48.56745');
insert into interval03 values ('1656 23:45:57.22332322');

--查看数据
select * from interval03;

--清理环境
drop table interval03;