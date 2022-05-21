-- @testpoint: hash_range二级分区表，使用参数创建表：压缩/约束/行迁移,部分测试点合理报错

--test1: 创建二级分区表：使用参数
--step1: 创建二级分区表，parameter fillfactor=80; expect:成功
drop table if exists t_subpartition_0014 cascade;
create table t_subpartition_0014(jid int,jn int,name varchar2)with(fillfactor=80) partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step2: 创建二级分区表，parameter orientation =row; expect:成功
drop table if exists t_subpartition_0014 cascade;
create table t_subpartition_0014(jid int,jn int,name varchar2)with(orientation=row) partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step3: 创建二级分区表，parameter orientation =column; expect:合理报错
drop table if exists t_subpartition_0014 cascade;
create table t_subpartition_0014(jid int,jn int,name varchar2)with(orientation=column) partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));

--test2: 创建二级分区表：使用压缩参数
--step4: 创建二级分区表，compress orientation=row; expect:合理报错
drop table if exists t_subpartition_0014 cascade;
create table t_subpartition_0014(jid int,jn int,name varchar2)compress partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));

--test3: 创建二级分区表：列约束结合参数和表空间
--step5: 创建二级分区表，唯一约束结合parameter fillfactor和表空间; expect:成功
drop table if exists t_subpartition_0014 cascade;
drop tablespace if exists ts_subpartition_0014;
create tablespace ts_subpartition_0014 relative location 'subpartition_tablespace/subpartition_tablespace_0014';
create table t_subpartition_0014(jid int,jn int unique with(fillfactor=80)using index tablespace ts_subpartition_0014,name varchar2)partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step6: 创建二级分区表，唯一约束的索引声明表空间; expect:成功
drop table if exists t_subpartition_0014 cascade;
create table t_subpartition_0014(jid int,jn int unique using index tablespace ts_subpartition_0014,name varchar2)partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step7: 创建二级分区表，主键约束结合parameter fillfactor和表空间; expect:成功
drop table if exists t_subpartition_0014 cascade;
create table t_subpartition_0014(jid int,jn int primary key with(fillfactor=80)using index tablespace ts_subpartition_0014,name varchar2)partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step8: 创建二级分区表，主键约束的索引声明表空间; expect:成功
drop table if exists t_subpartition_0014 cascade;
create table t_subpartition_0014(jid int,jn int primary key using index tablespace ts_subpartition_0014,name varchar2)partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));

--test4: 创建二级分区表：表约束结合参数和表空间
--step9: 创建二级分区表，唯一约束结合parameter fillfactor和表空间; expect:成功
drop table if exists t_subpartition_0014 cascade;
create table t_subpartition_0014(jid int,jn int,name varchar2, unique(jn)with(fillfactor=80)using index tablespace ts_subpartition_0014)partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step10: 创建二级分区表，唯一约束的索引声明表空间; expect:成功
drop table if exists t_subpartition_0014 cascade;
create table t_subpartition_0014(jid int,jn int,name varchar2, unique(jn)using index tablespace ts_subpartition_0014)partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step11: 创建二级分区表，主键约束结合parameter fillfactor和表空间; expect:成功
drop table if exists t_subpartition_0014 cascade;
create table t_subpartition_0014(jid int,jn int,name varchar2,primary key(jn)with(fillfactor=80)using index tablespace ts_subpartition_0014)partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step12: 创建二级分区表，主键约束的索引声明表空间; expect:成功
drop table if exists t_subpartition_0014 cascade;
create table t_subpartition_0014(jid int,jn int,name varchar2,primary key(jn)using index tablespace ts_subpartition_0014)partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));

--test5: 创建二级分区表：行迁移开，更新一级分区键数据
--step13: 创建二级分区表，行迁移开，并插入数据; expect:成功
drop table if exists t_subpartition_0014 cascade;
create table t_subpartition_0014(jid int,jn int,name varchar2)partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)))enable row movement;
insert into t_subpartition_0014 values(1,2,'jade'),(1,3,'tjade');
--step14: 查询一级分区数据; expect:成功
select * from t_subpartition_0014 partition(hr2);
--step15: 更新一级分区键为范围内数据; expect:成功
update t_subpartition_0014 set jid=0 where name='tjade';
--step16: 查询一级分区数据; expect:成功，分区没更新，hr2数据条数没变化
select * from t_subpartition_0014 partition(hr2);
--step17: 更新一级分区键为范围外数据; expect:成功
update t_subpartition_0014 set jid=16 where name='tjade';
--step18: 查询一级分区数据; expect:成功，分区更新，hr2少一条数据
select * from t_subpartition_0014 partition(hr2);

--test6: 创建二级分区表：行迁移开，更新二级分区键数据
--step19: 创建二级分区表，行迁移开，并插入数据; expect:成功
drop table if exists t_subpartition_0014 cascade;
create table t_subpartition_0014(jid int,jn int,name varchar2)partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)))enable row movement;
insert into t_subpartition_0014 values(1,2,'jade'),(1,3,'tjade');
--step20: 查询二级分区数据; expect:成功
select * from t_subpartition_0014 subpartition(hr21);
--step21: 更新二级分区键为范围内数据; expect:成功
update t_subpartition_0014 set jn=4 where name='tjade';
--step22: 查询二级分区数据; expect:成功，分区没更新，hr21数据条数没变化
select * from t_subpartition_0014 subpartition(hr21);
--step23: 更新二级分区键为范围内数据; expect:成功
update t_subpartition_0014 set jn=16 where name='tjade';
--step24: 查询二级分区数据; expect:成功，分区更新，hr21少一条数据
select * from t_subpartition_0014 subpartition(hr21);

--test7: 创建二级分区表：行迁移关，更新一级分区键数据
--step25: 创建二级分区表，行迁移关，并插入数据; expect:成功
drop table if exists t_subpartition_0014 cascade;
create table t_subpartition_0014(jid int,jn int,name varchar2)partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)))disable row movement;
insert into t_subpartition_0014 values(1,2,'jade'),(1,3,'tjade');
--step26: 查询一级分区数据; expect:成功
select * from t_subpartition_0014 partition(hr2);
--step27: 更新一级分区键为范围内数据; expect:成功
update t_subpartition_0014 set jid=2 where name='tjade';
--step28: 查询一级分区数据; expect:成功，分区没更新，hr2数据条数没变化
select * from t_subpartition_0014 partition(hr2);
--step29: 更新一级分区键为范围外数据; expect:合理报错
update t_subpartition_0014 set jid=16 where name='tjade';
--step30: 查询一级分区数据; expect:成功，分区更新，hr2数据条数没变化
select * from t_subpartition_0014 partition(hr2);

--test8: 创建二级分区表：行迁移关，更新二级分区键数据
--step31: 创建二级分区表，行迁移关，并插入数据; expect:成功
drop table if exists t_subpartition_0014 cascade;
create table t_subpartition_0014(jid int,jn int,name varchar2)partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)))disable row movement;
insert into t_subpartition_0014 values(1,2,'jade'),(1,3,'tjade');
--step32: 查询二级分区数据; expect:成功
select * from t_subpartition_0014 subpartition(hr21);
--step33: 更新二级分区键为范围内数据; expect:成功
update t_subpartition_0014 set jn=4 where name='tjade';
--step34: 查询二级分区数据; expect:成功，分区没更新，hr21数据条数没变化
select * from t_subpartition_0014 subpartition(hr21);
--step35: 更新二级分区键为范围内数据; expect:合理报错
update t_subpartition_0014 set jn=16 where name='tjade';
--step36: 查询二级分区数据; expect:成功，分区更新，hr21数据条数没变化
select * from t_subpartition_0014 subpartition(hr21);

--step37: 删除表; expect:成功
drop table if exists t_subpartition_0014 cascade;
drop tablespace if exists ts_subpartition_0014;