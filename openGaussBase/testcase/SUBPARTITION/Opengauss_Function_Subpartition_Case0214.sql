-- @testpoint: range_list二级分区表修改：add字段/drop字段/add约束,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0214;
drop tablespace if exists ts_subpartition_0214;
create tablespace ts_subpartition_0214 relative location 'subpartition_tablespace/subpartition_tablespace_0214';

--test1: alter table add/drop --字段
--step2: 创建表空间; expect:成功
create table if not exists t_subpartition_0214
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0214
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_list_1_1 values ( '-1','-2','-3','-4','-5'),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_list_2_1 values ( '6','7','8','9','10'),
    subpartition p_list_2_2 values ( default )
  ),
   partition p_range_3 values less than( 30 )
   (
    subpartition p_list_3_1 values ( default )
  ),
   partition p_range_4 values less than( 40 )
   (
    subpartition p_list_4_1 values ( default )
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step3: 修改二级分区表,添加列; expect:成功
alter table t_subpartition_0214 add column col_5 int;
--step4: 插入数据; expect:成功
insert into t_subpartition_0214 values(1,8,1,1,1),(4,7,4,4,4),(5,8,5,5,5),(8,9,8,8,8),(9,9,9,9,9); 
--step5: 修改二级分区表,删除列; expect:成功
alter table t_subpartition_0214 drop column col_5 ;

--test2: alter table add --约束
--step6: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0214;
create table if not exists t_subpartition_0214
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0214
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_list_1_1 values ( '-1','-2','-3','-4','-5'),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_list_2_1 values ( '6','7','8','9','10'),
    subpartition p_list_2_2 values ( default )
  ),
   partition p_range_3 values less than( 30 )
   (
    subpartition p_list_3_1 values ( default )
  ),
   partition p_range_4 values less than( 40 )
   (
    subpartition p_list_4_1 values ( default )
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step7: 修改二级分区表,添加check约束; expect:成功
alter table t_subpartition_0214 add constraint constraint_check check (col_3 is not null);

--step8: 创建索引并插入数据; expect:成功
drop index if exists index_01;
create index index_01 on t_subpartition_0214(col_1,col_2);
insert into t_subpartition_0214 values(1,8,1,1),(4,7,4,4),(5,8,5,5),(8,9,8,8),(9,9,9,9);
--step9: 使用索引添加主键; expect:合理报错
alter table  t_subpartition_0214 add  primary key (col_2) using index ppp;
--step10: 使用索引添加唯一约束; expect:合理报错
alter table  t_subpartition_0214 add  unique (col_1) using index uuu;

--step11: 添加约束; expect:成功
alter table  t_subpartition_0214 add  constraint aaa check(col_1 is not null) not valid ;
--step12: 验证检查类约束; expect:成功
alter table  t_subpartition_0214 validate constraint aaa;
--step13: 删除约束; expect:成功
alter table  t_subpartition_0214 drop constraint if exists aaa;

--step14: 添加索引; expect:合理报错
alter table  t_subpartition_0214  add index index_01 (col_2);
--step15: cluster添加默认索引; expect:合理报错
alter table  t_subpartition_0214 cluster on index_01;
--step16: 新建用户; expect:成功
create user u_subpartition_0214 password 'test@123';
--step17: 表的属主修改为指定用户; expect:成功
alter table  t_subpartition_0214 owner to u_subpartition_0214;
--step18: 修改表的压缩特性nocompress; expect:成功
alter table  t_subpartition_0214 set nocompress;
--step19: 修改表的行访问控制开关disable row level security; expect:合理报错
alter table  t_subpartition_0214 disable row level security;
--step20: 强制修改表的行访问控制开关no force row level security; expect:合理报错
alter table  t_subpartition_0214  no force row level security;

--step21: 插入数据; expect:成功
insert into t_subpartition_0214 values(30,8,1,1),(29,9,9,9);
--step22: 修改表的行迁移开关disable row movement; expect:成功
alter table t_subpartition_0214 disable row movement;
--step23: 更新数据至分区外; expect:合理报错
update t_subpartition_0214  set col_1=1 where col_1=30;
--step24: 修改表的行迁移开关enable row movement; expect:成功
alter table t_subpartition_0214 enable row movement;
--step25: 更新数据至分区外; expect:成功
update t_subpartition_0214  set col_1=1 where col_1=30;

--step26: 清理环境; expect:成功
drop user if exists u_subpartition_0214 cascade;
drop table if exists t_subpartition_0214;
drop tablespace if exists ts_subpartition_0214;