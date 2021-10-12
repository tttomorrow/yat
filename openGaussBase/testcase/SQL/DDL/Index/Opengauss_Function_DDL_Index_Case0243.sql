-- @testpoint: 列分区表创建bree索引,合理报错

--1. 创建表
create table tb_btree_partition(id int,name varchar) WITH (ORIENTATION = column)
PARTITION BY RANGE(id)(
        PARTITION P1 VALUES LESS THAN(100),
        PARTITION P2 VALUES LESS THAN(1000),
        PARTITION P3 VALUES LESS THAN(MAXVALUE))
;
--2. 插入数据
insert into tb_btree_partition values (generate_series(1,20000), 'test');
--3.创建索引
create index part_idx on tb_btree_partition using btree(id) local (partition p1, partition p2, partition p3) where id>500;
create index part_idx_global on tb_btree_partition using btree(id) global ;
create index team_idx on tb_btree_partition using btree(id, name) local (partition p1, partition p2, partition p3);
create index exp_idx on tb_btree_partition using btree((id+1))  local (partition p1, partition p2, partition p3);
create index exp_idx on tb_btree_partition using btree((id+1))  global;

--4.查询索引
SET ENABLE_SEQSCAN=off;
explain select count(*) from tb_btree_partition where id>5 and name = 'ess';

--tearDown
drop table if exists tb_btree_partition cascade;
