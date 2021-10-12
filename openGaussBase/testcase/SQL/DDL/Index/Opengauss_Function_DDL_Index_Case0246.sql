-- @testpoint: 列存分区表创建psort 组合索引,合理报错

--1. 创建表
create table tb_partition(id int,name varchar) WITH (ORIENTATION = column)
PARTITION BY RANGE(id)(
        PARTITION P1 VALUES LESS THAN(100),
        PARTITION P2 VALUES LESS THAN(1000),
        PARTITION P3 VALUES LESS THAN(MAXVALUE))
;
--2. 插入数据
insert into tb_partition values (generate_series(1,20000), 'test');
--3.创建索引
create index team_idx on tb_partition using psort(id, name) local (partition p1, partition p2, partition p3);
--4.查询索引
SET ENABLE_SEQSCAN=off;
explain select count(*) from tb_partition where id>5 and name = 'ess';
--5.创建全局索引
drop index if exists team_idx;
create index team_idx_global on tb_partition using  psort(id, name) global;
--6.创建表达式索引
drop index if exists team_idx;
create index team_idx on tb_partition using psort((id*2)) local (partition p1, partition p2, partition p3);
create index team_idx on tb_partition using psort((id*2)) global;

--tearDown
drop table if exists tb_partition cascade;