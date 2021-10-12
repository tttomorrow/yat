-- @testpoint: interval时间间隔类型，天数和秒数精度定义在合理范围内

--创建表
drop table if exists interval01;
create table interval01 (name interval day(2) to second(3));

--插入数据
insert into interval01 values ('13 2:25:45.325');
insert into interval01 values ('2 18:50:33.6623');

--查看数据
select * from interval01;

--清理环境
drop table interval01;


