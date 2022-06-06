-- @testpoint: 创建快照后删除不存在的快照,合理报错

--step1:建表并插入数据;expect: 建表并插入数据成功
drop table if exists t_snapshot_tab_0004;
create table t_snapshot_tab_0004(id int, name varchar);
insert into t_snapshot_tab_0004 values (1,'zhangsan'),(2,'lisi'),(3,'wangwu'),(4,'lisa'),(5,'jack');

--step2:创建快照;expect: 创建成功
create snapshot s_snapshot_s1@1.0 comment is 'first version' as select * from t_snapshot_tab_0004;

--step3:删除数据表快照;expect: 报错提示快照不存在
purge snapshot s_snapshot_s1@3.0;

--step4:发布数据表快照;expect: 报错提示快照不存在
select * from public.s_snapshot_s1@3.0;

--step5:存档数据表快照;expect: 报错提示快照不存在
archive snapshot s_snapshot_s1@3.0;

--step6:清理环境;expect: 清理成功
purge snapshot s_snapshot_s1@1.0;
drop table t_snapshot_tab_0004;