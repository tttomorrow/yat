-- @testpoint: 验证hash分区表analyze分区语法，部分场景合理报错

drop table if exists t_b_analyze_par_0019;
create table t_b_analyze_par_0019(c1 int,c2 int)
partition by hash(c1) (
  partition p1,
  partition p2,
  partition p3,
  partition p4,
  partition p5,
  partition p6,
  partition p7,
  partition p8,
  partition p9,
  partition p10
  );
create index i_b_analyze_par_0019_1 on t_b_analyze_par_0019 (c1) global;
create index i_b_analyze_par_0019_2 on t_b_analyze_par_0019 (c2) local;
insert into t_b_analyze_par_0019 values
  (2,1),
  (3,2),
  (5,3),
  (9,4),
  (34,5),
  (35,6);

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_analyze_par_0019') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_analyze_par_0019')) order by relname;

-- analyze一个分区，验证成功
alter table t_b_analyze_par_0019 analyze partition p2;
-- analyze多个分区，验证成功
alter table t_b_analyze_par_0019 analyze partition p3,p4;
-- analyze所有分区，验证成功
alter table t_b_analyze_par_0019 analyze partition all;
-- analyze无数据分区，验证成功
alter table t_b_analyze_par_0019 analyze partition p1;
-- analyze不存在分区，合理报错
alter table t_b_analyze_par_0019 analyze partition pnull;

select * from t_b_analyze_par_0019 order by c1;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_analyze_par_0019') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_analyze_par_0019')) order by relname;

-- 清理环境
drop table t_b_analyze_par_0019;

