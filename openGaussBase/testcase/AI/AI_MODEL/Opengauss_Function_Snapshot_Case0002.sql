-- @testpoint: sample snapshot --创建训练集与测试集,部分测试点合理报错

--step1:建表并插入数据;expect: 建表并插入数据成功
drop table if exists t_snaphot_tab_0002;
create table t_snaphot_tab_0002(id int, name varchar);
insert into t_snaphot_tab_0002 values (1,'zhangsan'),(2,'lisi'),(3,'wangwu'),(4,'lisa'),(5,'jack');

--step2:创建快照;expect: 创建成功
create snapshot s_snapshot_s1@1.0 comment is 'first version' as select * from t_snaphot_tab_0002;

--step3:创建训练集与测试集;expect: 创建成功
sample snapshot s_snapshot_s1@1.0 stratify by name as _test at ratio .2, as _train at ratio .8 comment is 'training';

--step4:删除数据表快照;expect: 删除失败，报错提示有依赖该快照的其他snapshot
purge snapshot s_snapshot_s1@1.0;

--step5:删除依赖快照;expect: 删除成功
purge snapshot s_snapshot_s1_train@1.0;
purge snapshot s_snapshot_s1_test@1.0;

--step6:删除数据表快照;expect: 删除成功
purge snapshot s_snapshot_s1@1.0;

--step7:清理环境;expect: 清理成功
drop table t_snaphot_tab_0002;