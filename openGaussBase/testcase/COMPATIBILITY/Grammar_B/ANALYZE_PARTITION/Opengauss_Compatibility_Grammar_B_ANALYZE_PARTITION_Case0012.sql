-- @testpoint: 验证range分区表analyze分区语法(压缩表)，部分场景合理报错

drop table if exists t_b_analyze_par_0012;
create table t_b_analyze_par_0012(c1 int primary key,c2 int)
with (orientation=column,compression=high)
partition by range(c1) (
  partition p1 values less than(100),
  partition p2 values less than(200),
  partition p3 values less than(300),
  partition p4 values less than(400),
  partition p5 values less than(500),
  partition p6 values less than(600),
  partition p7 values less than(700),
  partition p8 values less than(800),
  partition p9 values less than(900),
  partition p10 values less than(1000)
  );
create index i_b_analyze_par_0012_1 on t_b_analyze_par_0012 (c2) global;
create index i_b_analyze_par_0012_2 on t_b_analyze_par_0012 (c1) local;
insert into t_b_analyze_par_0012 values
  (101,101),
  (201,201),
  (301,301),
  (401,401),
  (501,501);

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_analyze_par_0012') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_analyze_par_0012')) order by relname;

-- analyze一个分区，验证成功
alter table t_b_analyze_par_0012 analyze partition p2;
select * from t_b_analyze_par_0012 partition(p2) order by c1;
-- analyze多个分区，验证成功
alter table t_b_analyze_par_0012 analyze partition p3,p4;
select * from t_b_analyze_par_0012 partition(p3) order by c1;
select * from t_b_analyze_par_0012 partition(p4) order by c1;
-- analyze所有分区，验证成功
alter table t_b_analyze_par_0012 analyze partition all;
select * from t_b_analyze_par_0012 order by c1;
-- analyze无数据分区，验证成功
alter table t_b_analyze_par_0012 analyze partition p10;
select * from t_b_analyze_par_0012 partition(p10) order by c1;
-- analyze不存在分区，合理报错
alter table t_b_analyze_par_0012 analyze partition pnull;
select * from t_b_analyze_par_0012 order by c1;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_analyze_par_0012') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_analyze_par_0012')) order by relname;

-- 清理环境
drop table t_b_analyze_par_0012;

