-- @testpoint: 验证增删分区原语法和MySQL兼容语法对全局临时表执行，合理报错
drop table if exists t_b_add_drop_par_0003;
create global temp table t_b_add_drop_par_0003(c1 int,c2 text);
insert into t_b_add_drop_par_0003 values(1,'a'),(2,'b'),(3,'c');
-- 原语法合理报错
alter table t_b_add_drop_par_0003 add partition p1 values less than (1); 
alter table t_b_add_drop_par_0003 add partition p1 values(1);
alter table t_b_add_drop_par_0003 add partition p1 values(1),add partition p2 values(2);
alter table t_b_add_drop_par_0003 drop partition p1,drop partition p2;
-- MySQL语法合理报错
alter table t_b_add_drop_par_0003 add partition (partition p1 values less than (1));
alter table t_b_add_drop_par_0003 add partition (partition p1 values(1));
alter table t_b_add_drop_par_0003 add partition (partition p1 values(1),partition p2 values(2));
alter table t_b_add_drop_par_0003 drop partition p1,p2;
drop table t_b_add_drop_par_0003;
