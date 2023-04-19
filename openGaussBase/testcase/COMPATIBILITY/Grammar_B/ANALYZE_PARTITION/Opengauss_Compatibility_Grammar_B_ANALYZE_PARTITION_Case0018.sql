-- @testpoint: 验证list分区表analyze分区语法(主表指定非默认tablespace)，部分场景合理报错

drop tablespace if exists ts_b_analyze_par_0018;
create tablespace ts_b_analyze_par_0018 relative location 'ts_b_analyze_par_0018';
drop table if exists t_b_analyze_par_0018;
create table t_b_analyze_par_0018(c1 int primary key,c2 int,c3 int)
tablespace ts_b_analyze_par_0018
partition by list(c1) (
  partition p1 values(1),
  partition p2 values(2),
  partition p3 values(3),
  partition p4 values(4),
  partition p5 values(5),
  partition p6 values(6),
  partition p7 values(7),
  partition p8 values(8),
  partition p9 values(9),
  partition p10 values(10)
  );
create index i_b_analyze_par_0018_1 ON t_b_analyze_par_0018 (c1) global;
create index i_b_analyze_par_0018_2 ON t_b_analyze_par_0018 (c2) local;
insert into t_b_analyze_par_0018 values
  (2,2),
  (3,3),
  (4,4),
  (5,5),
  (6,6);

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_analyze_par_0018') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_analyze_par_0018')) order by relname;

-- analyze一个分区，验证成功
alter table t_b_analyze_par_0018 analyze partition p2;
select * from t_b_analyze_par_0018 partition(p2) order by c1;
-- analyze多个分区，验证成功
alter table t_b_analyze_par_0018 analyze partition p3,p4;
select * from t_b_analyze_par_0018 partition(p3) order by c1;
select * from t_b_analyze_par_0018 partition(p4) order by c1;
-- analyze所有分区，验证成功
alter table t_b_analyze_par_0018 analyze partition all;
select * from t_b_analyze_par_0018 order by c1;
-- analyze无数据分区，验证成功
alter table t_b_analyze_par_0018 analyze partition p10;
select * from t_b_analyze_par_0018 partition(p10) order by c1;
-- analyze不存在分区，合理报错
alter table t_b_analyze_par_0018 analyze partition pnull;
select * from t_b_analyze_par_0018 order by c1;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_analyze_par_0018') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_analyze_par_0018')) order by relname;

-- 清理环境
drop table t_b_analyze_par_0018;
drop tablespace ts_b_analyze_par_0018;

