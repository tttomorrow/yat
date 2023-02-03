-- @testpoint: 验证ADD PARTITION指定列为其它列，合理报错

drop table if exists t_b_add_drop_par_0007;
create table t_b_add_drop_par_0007(c1 int,c2 int)
partition by range(c1) (
  partition p1 start(1) end(10000),
  partition p2 start(10000) end(20000),
  partition p3 start(20000) end(40000)
  );

alter table t_b_add_drop_par_0007 add partition p4 column c2 values less than(50000);
alter table t_b_add_drop_par_0007 add partition (partition p4 column c2 values less than(50000));

drop table t_b_add_drop_par_0007;

