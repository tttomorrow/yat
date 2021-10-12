-- @testpoint: 插入日期类型数据，违法唯一约束，合理报错
-- @modify at: 2020-11-16
--建表
drop table if exists t_date5;
CREATE TABLE t_date5(c1 int,c2 integer ,c3 date,c4 timestamp with time zone);
--创建索引
drop index if exists idx_t_date5;
create unique index idx_t_date5 on t_date5(c3,c4);
--插入数据
insert into  t_date5 values(2, 10, '2017-10-10', '2017-10-10 00:00:00.000000 +08:00');
insert into  t_date5 values(2, 10, '2017-10-10', '2017-11-10 00:00:00.000000 +08:00');
insert into  t_date5 values(2, 10, '2017-11-10', '2017-10-10 00:00:00.000000 +08:00');
--再次插入数据，合理报错
insert into  t_date5 values(2, 10, '2017-11-10', '2017-10-10 01:00:00.000000 +09:00');
--查询表信息
select distinct c4 from t_date5 order by c4;
select max(c4) from t_date5 group by c4;
select min(c4) from t_date5 group by c4;
--删表
drop table if exists t_date5 cascade;