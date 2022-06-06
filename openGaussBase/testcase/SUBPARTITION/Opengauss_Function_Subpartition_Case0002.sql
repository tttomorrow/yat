-- @testpoint: hash_hash二级分区键列约束测试:列存储/唯一约束/非空约束/默认值/check约束/主键/外键,部分测试点合理报错

--test1: 二级分区不支持列存储
--step1: 创建二级分区列存表; expect:报错，不支持
drop table if exists t_subpartition_0002 cascade;
create table t_subpartition_0002(jid int,jn int,name varchar2)with(orientation=column)partition by hash (jid) subpartition by hash(jn)(partition hr1(subpartition hr1_1 ,subpartition hr1_2 ));

--test2: 二级分区键列约束:主键,插入/更新重复数据
--step2: 创建二级分区表，二级分区键包含列约束主键; expect:成功
drop table if exists t_subpartition_0002 cascade;
create table t_subpartition_0002(jid int,jn int primary key,name varchar2)partition by hash (jid) subpartition by hash(jn)
(partition hr1(subpartition hr11 ,subpartition hr12 ),partition hr2(subpartition hr21 ,subpartition hr22 ));
--step3: 插入数据; expect:成功
insert into t_subpartition_0002 values(1,1,'jade');
--step4: 插入重复数据; expect:合理报错
insert into t_subpartition_0002 values(1,1,'jade');
--step5: 插入数据; expect:成功
insert into t_subpartition_0002 values(1,2,'jade2');
--step6: 更新为重复数据; expect:合理报错
update t_subpartition_0002 set jn=1 where name='jade2';

--test3: 二级分区键列约束:唯一约束,插入/更新重复数据
--step7: 创建二级分区表，二级分区键包含列唯一约束; expect:成功
drop table if exists t_subpartition_0002 cascade;
create table t_subpartition_0002(jid int,jn int unique,name varchar2)partition by hash (jid) subpartition by hash(jn)
(partition hr1(subpartition hr11 ,subpartition hr12 ),partition hr2(subpartition hr21 ,subpartition hr22 ));
--step8: 插入数据; expect:成功
insert into t_subpartition_0002 values(1,1,'jade');
--step9: 插入重复数据; expect:合理报错
insert into t_subpartition_0002 values(1,1,'jade');
--step10: 插入数据; expect:成功
insert into t_subpartition_0002 values(1,2,'jade2');
--step11: 更新为重复数据; expect:合理报错
update t_subpartition_0002 set jn=1 where name='jade2';

--test4: 二级分区键列约束:非空约束,插入/更新数据
--step12: 创建二级分区表，二级分区键包含列非空约束; expect:成功
drop table if exists t_subpartition_0002 cascade;
create table t_subpartition_0002(jid int,jn int not null,name varchar2)partition by hash (jid) subpartition by hash(jn)
(partition hr1(subpartition hr11 ,subpartition hr12 ),partition hr2(subpartition hr21 ,subpartition hr22 ));
--step13: 插入非空数据; expect:成功
insert into t_subpartition_0002 values(1,1,'jade');
--step14: 插入非空数据; expect:成功
insert into t_subpartition_0002 values(1,2,'jade2');
--step15: 更新为非空数据; expect:成功
update t_subpartition_0002 set jn=1 where name='jade2';
--step16: 插入空数据; expect:合理报错
insert into t_subpartition_0002(jid,jn,name) values(1,null,'jade');
--step17: 更新为非空数据; expect:合理报错
update t_subpartition_0002 set jn=null;

--test5: 二级分区键列约束:默认为null,插入非空/空数据
--step18: 创建二级分区表，二级分区键列约束默认为null; expect:成功
drop table if exists t_subpartition_0002 cascade;
create table t_subpartition_0002(jid int,jn int null,name varchar2)partition by hash (jid) subpartition by hash(jn)
(partition hr1(subpartition hr11 ,subpartition hr12 ),partition hr2(subpartition hr21 ,subpartition hr22 ));
--step19: 插入非空数据; expect:成功
insert into t_subpartition_0002(jid,jn,name) values(1,2,'jade');
--step20: 插入空数据; expect:成功
insert into t_subpartition_0002(jid,jn,name) values(1,null,'jade');

--test6: 二级分区键列约束:check约束,插入符合/不符合check数据
--step21: 创建二级分区表，二级分区键包含列check约束; expect:成功
drop table if exists t_subpartition_0002 cascade;
create table t_subpartition_0002(jid int,jn int check(jn>6),name varchar2)partition by hash (jid) subpartition by hash(jn)
(partition hr1(subpartition hr11 ,subpartition hr12 ),partition hr2(subpartition hr21 ,subpartition hr22 ));
--step22: 插入符合check的数据; expect:成功
insert into t_subpartition_0002(jid,jn,name) values(1,8,'jade');
--step23: 插入不符合check的数据; expect:合理报错
insert into t_subpartition_0002(jid,jn,name) values(1,6,'jade');

--test7: 二级分区键列约束:默认值,二级分区键有无值插入数据
--step24: 创建二级分区表，二级分区键包含列约束默认值; expect:成功
drop table if exists t_subpartition_0002 cascade;
create table t_subpartition_0002(jid int,jn int default 6,name varchar2)partition by hash (jid) subpartition by hash(jn)
(partition hr1(subpartition hr11 ,subpartition hr12 ),partition hr2(subpartition hr21 ,subpartition hr22 ));
--step25: 插入数据,二级分区键无值; expect:成功
insert into t_subpartition_0002(jid,name)values(1,'jade');
--step26: 插入数据,二级分区键有值; expect:成功
insert into t_subpartition_0002(jid,jn,name)values(1,8,'jade');

--test8: 二级分区键列约束:外键
--step27: 创建二级分区表，二级分区键包含列约束外键; expect:成功
drop table if exists t_subpartition_0002_01 cascade;
drop table if exists t_subpartition_0002 cascade;
create table if not exists t_subpartition_0002_01(jid int,jn int primary key,name varchar2);
create table t_subpartition_0002(jid int,jn int references t_subpartition_0002_01(jn),name varchar2)partition by hash (jid) subpartition by hash(jn)
(partition hr1(subpartition hr11 ,subpartition hr12 ),partition hr2(subpartition hr21 ,subpartition hr22 ));
--step28: 插入数据,二级分区键值存在; expect:成功
insert into t_subpartition_0002_01(jid,jn,name)values(1,8,'jade'),(1,9,'jade');
insert into t_subpartition_0002(jid,jn,name)values(1,8,'jade');
--step29: 插入数据,二级分区键值不存在; expect:合理报错
insert into t_subpartition_0002(jid,jn,name)values(1,6,'jade');
--step30: 更新数据,二级分区键值存在; expect:成功
update t_subpartition_0002 set jn =8 where name='jade';
--step31: 更新数据,二级分区键值不存在; expect:合理报错
update t_subpartition_0002 set jn =16 where name='jade';

--step32: 删除表; expect:成功
drop table if exists t_subpartition_0002 cascade;
drop table if exists t_subpartition_0002_01 cascade;