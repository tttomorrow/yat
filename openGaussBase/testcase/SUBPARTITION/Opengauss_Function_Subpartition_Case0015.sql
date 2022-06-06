-- @testpoint: hash_range创建和修改二级分区表,查询数据,执行操作analyzevacuum/cluster,部分测试点合理报错

--test1: 创建二级分区表,分区名和分区键约束
--step1: 创建二级分区表,没有一级分区名和二级分区名; expect:合理报错
drop table if exists t_subpartition_0015 cascade;
create table t_subpartition_0015(jid int,jn int,name varchar2)partition by hash (jid) subpartition by range(jn)();
--step2: 创建二级分区表,有一个一级分区名和一个二级分区名; expect:成功
drop table if exists t_subpartition_0015 cascade;
create table t_subpartition_0015(jid int,jn int,name varchar2)partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6)));
--step3: 创建二级分区表,有两个一级分区键; expect:合理报错
drop table if exists t_subpartition_0015 cascade;
create table t_subpartition_0015(jid int,jn int,name varchar2)partition by hash (jid,jn) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6)));
--step4: 创建二级分区表,有两个二级分区键; expect:合理报错
drop table if exists t_subpartition_0015 cascade;
create table t_subpartition_0015(jid int,jn int,name varchar2)partition by hash (jid) subpartition by range(jid,jn)
(partition hr1(subpartition hr11 values less than(6)));
--step5: 创建二级分区表,有两个一级分区键,没有二级分区键; expect:合理报错
drop table if exists t_subpartition_0015 cascade;
create table t_subpartition_0015(jid int,jn int,name varchar2)partition by hash (jid) partition by range(jn)
(partition hr1(subpartition hr11 values less than(6)));
--step6: 创建二级分区表,一级分区键和二级分区键相同; expect:合理报错
drop table if exists t_subpartition_0015 cascade;
create table t_subpartition_0015(jid int,jn int,name varchar2)partition by hash (jn) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)))disable row movement;
--step7: 创建二级分区表,一级分区名和二级分区名相同; expect:合理报错
drop table if exists t_subpartition_0015 cascade;
create table t_subpartition_0015(jid int,jn int,name varchar2)partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr1 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)))disable row movement;

--test2: 创建分区表,使用关键字like源表是分区表
--step8: 创建一级分区表; expect:成功
drop table if exists like_t_subpartition_0015 cascade;
create table if not exists like_t_subpartition_0015(jid int,jn int,name varchar2)partition by hash (jid)(partition hr1,partition hr2);
--step9: 创建一级分区表,关键字like源表是一级分区表; expect:合理报错
drop table if exists t_subpartition_0015 cascade;
create table if not exists t_subpartition_0015(like like_t_subpartition_0015 including partition);
--step10: 创建二级分区表; expect:成功
drop table if exists like_t_subpartition_0015 cascade;
create table like_t_subpartition_0015(jid int,jn int,name varchar2)partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)))disable row movement;
--step11: 创建二级分区表,关键字like源表是二级分区表; expect:合理报错
drop table if exists t_subpartition_0015 cascade;
create table if not exists t_subpartition_0015(like like_t_subpartition_0015 including partition);

--test3: 修改分区表,添加分区
--step12: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0015 cascade;
create table t_subpartition_0015(jid int,jn int ,name varchar2)partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step13: 修改分区表,添加二级分区; expect:合理报错
alter table if exists t_subpartition_0015 add subpartition hr13 values less than(maxvalue);
--step14: 修改分区表,添加一级分区; expect:合理报错
alter table if exists t_subpartition_0015 add partition hr3;

--test4: 使用rownum/order by/group by/subquery查询数据
--step15: 创建二级分区表且插入数据; expect:成功
drop table if exists t_subpartition_0015 cascade;
create table t_subpartition_0015(jid int,jn int ,name varchar2)partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
insert into t_subpartition_0015 values(0,0,'jade'),(0,1,'jade'),(0,2,'jade'),(0,3,'jade'),(0,4,'jade');
insert into t_subpartition_0015 values(1,10,'jade'),(1,11,'jade'),(1,12,'jade'),(1,13,'jade'),(1,14,'jade');
--step16: 使用rownum和order by查询数据; expect:成功
select * from t_subpartition_0015 where rownum<6 order by jn;
--step17: 使用order by查询数据; expect:成功
select * from t_subpartition_0015 order  by jn;
--step18: 使用group by查询数据; expect:成功
select name,sum(jn) from t_subpartition_0015 group  by name;
--step19: 使用subquery查询数据; expect:成功
select * from t_subpartition_0015 where name in(select name from t_subpartition_0015 where jn>=11);

--test5: analyze verbose操作
--step20: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0015 cascade;
create table t_subpartition_0015(jid int,jn int ,name varchar2)partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step21: 分析表统计信息,并输出相关信息; expect:成功
analyze verbose t_subpartition_0015;
--step22: 分析表(列)的统计信息,并输出相关信息; expect:成功
analyze verbose t_subpartition_0015(jn);
--step23: 查询系统表; expect:成功,系统表未记录
select * from pg_statistic where starelid=(select oid from pg_class where relname='t_subpartition_0015');
select * from pg_stats  where tablename='t_subpartition_0015';
--step24: 分析的一级分区统计信息,并输出相关信息; expect:成功
analyze verbose t_subpartition_0015 partition(hr1);
--step25: 分析表的二级分区统计信息,并输出相关信息; expect:合理报错
analyze verbose t_subpartition_0015 subpartition(hr11);

--test6: vacuum verbose操作
--step26: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0015 cascade;
create table t_subpartition_0015(jid int,jn int ,name varchar2)partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step27: 对表执行vacuum操作,并输出相关信息; expect:成功
vacuum verbose t_subpartition_0015;
--step28: 对表(列)执行vacuum操作,并输出相关信息; expect:合理报错
vacuum verbose t_subpartition_0015(jn);
--step29: 插入数据; expect:成功
insert into t_subpartition_0015 values(0,0,'jade'),(0,1,'jade'),(0,2,'jade'),(0,3,'jade'),(0,4,'jade');
insert into t_subpartition_0015 values(1,10,'jade'),(1,11,'jade'),(1,12,'tjade'),(1,13,'tjade'),(1,14,'tjade');
--step30: 对一级分区执行vacuum操作,并输出相关信息; expect:成功
vacuum verbose t_subpartition_0015 partition(hr1);
--step31: 对二级分区执行vacuum操作,并输出相关信息; expect:成功
vacuum verbose t_subpartition_0015 subpartition(hr11);
--step32: 查看系统表; expect:成功
select schemaname,relname,last_analyze,analyze_count,last_data_changed from pg_stat_all_tables where relname='t_subpartition_0015';

--test7: vaccum analyze verbose操作
--step33: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0015 cascade;
create table t_subpartition_0015(jid int,jn int ,name varchar2)partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step34: 对表(列)执行vacuum analyze操作,并输出相关信息; expect:成功
vacuum analyze verbose t_subpartition_0015(jn);

--test8: cluster操作(不支持)
--step35: 创建二级分区表并创建二级分区键索引; expect:成功
drop table if exists t_subpartition_0015 cascade;
create table t_subpartition_0015(jid int,jn int unique ,name varchar2)partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
create unique index idxjade on t_subpartition_0015(jn);
--step36: 对二级分区表执行cluster操作; expect:合理报错
cluster verbose t_subpartition_0015 using idxjade;
--step37: 重建索引; expect:成功
reindex index idxjade;
--step38: 执行cluster操作; expect:合理报错
cluster verbose t_subpartition_0015;
--step39: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0015 cascade;
create table t_subpartition_0015(jid int,jn int unique ,name varchar2)partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step40: 对一级分区执行cluster操作; expect:合理报错
cluster verbose t_subpartition_0015 partition(hr1);
--step41: 对二级分区执行cluster操作; expect:合理报错
cluster verbose t_subpartition_0015 subpartition(hr11);
--step42: 对表(列)执行cluster analyze操作; expect:合理报错
cluster analyze verbose t_subpartition_0015(jn);
--step43: 对表(列,列)执行cluster操作; expect:合理报错
cluster verbose t_subpartition_0015(jid,jn);

--step44: 删除表; expect:成功
drop table if exists t_subpartition_0015 cascade;
