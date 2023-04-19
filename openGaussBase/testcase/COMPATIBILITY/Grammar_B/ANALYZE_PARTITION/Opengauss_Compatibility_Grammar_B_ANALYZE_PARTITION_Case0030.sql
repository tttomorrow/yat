-- @testpoint: 验证range-list分区表analyze分区语法(主表指定非默认tablespace)，部分场景合理报错

drop tablespace if exists ts_b_analyze_par_0030;
create tablespace ts_b_analyze_par_0030 relative location 'ts_b_analyze_par_0030';
drop table if exists t_b_analyze_par_0030;
create table t_b_analyze_par_0030(c1 int primary key,c2 char(1),c3 int)
tablespace ts_b_analyze_par_0030
partition by range(c1) subpartition by list(c2) 
(
  partition p1 values less than (100)
  (
    subpartition p1_1 values ('a'),
    subpartition p1_2 values ('b')
  ),
  partition p2 values less than (200)
  (
    subpartition p2_1 values ('c'),
    subpartition p2_2 values ('d')
  ),
  partition p3 values less than (300)
  (
    subpartition p3_1 values ('e'),
    subpartition p3_2 values ('f')
  )
);
create index i_b_analyze_par_0030_1 on t_b_analyze_par_0030 (c1) global;
create index i_b_analyze_par_0030_2 on t_b_analyze_par_0030 (c2) local;
insert into t_b_analyze_par_0030 values
  (1,'a',1),
  (2,'b',2),
  (101,'c',3),
  (102,'d',4);

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_analyze_par_0030') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_analyze_par_0030')) order by relname;

-- analyze一个分区，验证成功
alter table t_b_analyze_par_0030 analyze partition p1;
select * from t_b_analyze_par_0030 partition(p1) order by c1;
-- analyze多个分区，验证成功
alter table t_b_analyze_par_0030 analyze partition p1,p2;
select * from t_b_analyze_par_0030 partition(p1) order by c1;
select * from t_b_analyze_par_0030 partition(p2) order by c1;
-- analyze所有分区，验证成功
alter table t_b_analyze_par_0030 analyze partition all;
select * from t_b_analyze_par_0030 order by c1;
-- analyze无数据分区，验证成功
alter table t_b_analyze_par_0030 analyze partition p3;
select * from t_b_analyze_par_0030 partition(p3) order by c1;
-- analyze不存在分区，合理报错
alter table t_b_analyze_par_0030 analyze partition pnull;
-- analyze二级分区，合理报错
alter table t_b_analyze_par_0030 analyze partition p1_1;
alter table t_b_analyze_par_0030 analyze subpartition p1_1;
alter table t_b_analyze_par_0030 analyze subpartition p1_1,p1_2;
alter table t_b_analyze_par_0030 analyze subpartition all;
select * from t_b_analyze_par_0030 order by c1;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_analyze_par_0030') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_analyze_par_0030')) order by relname;

-- 清理环境
drop table t_b_analyze_par_0030;
drop tablespace ts_b_analyze_par_0030;

