-- @testpoint: hash_range二级分区键表约束测试:主键/唯一约束/check约束/外键

--test1: 二级分区键表约束:主键
--step1: 创建二级分区表，主键为二级分区键; expect:成功
drop table if exists t_subpartition_0012 cascade;
create table t_subpartition_0012(jid int,jn int,name varchar2,constraint hrjpk primary key(jn))partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step2: 创建二级分区表，主键为二级分区键和一级分区键,第一位是二级分区键; expect:成功
drop table if exists t_subpartition_0012 cascade;
create table t_subpartition_0012(jid int,jn int,name varchar2,constraint hrjpk primary key(jn,jid))partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step3: 创建二级分区表，主键为二级分区键和一级分区键,第一位是一级分区键; expect:成功
drop table if exists t_subpartition_0012 cascade;
create table t_subpartition_0012(jid int,jn int,name varchar2,constraint hrjpk primary key(jid,jn))partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step4: 创建二级分区表，主键为一级分区键和二级分区键和普通列,第一位是一级分区键; expect:成功
drop table if exists t_subpartition_0012 cascade;
create table t_subpartition_0012(jid int,jn int,name varchar2,constraint hrjpk primary key(jid,jn,name))partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step5: 创建二级分区表，主键为二级分区键和一级分区键和普通列,第一位是二级分区键; expect:成功
drop table if exists t_subpartition_0012 cascade;
create table t_subpartition_0012(jid int,jn int,name varchar2,constraint hrjpk primary key(jn,jid,name))partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));

--test2: 二级分区键表约束:唯一约束
--step6: 创建二级分区表，唯一约束：二级分区键确认约束名; expect:成功
drop table if exists t_subpartition_0012 cascade;
create table t_subpartition_0012(jid int,jn int,name varchar2,constraint hrjpk unique(jn))partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step7: 创建二级分区表，唯一约束：一级分区键为默认约束名; expect:成功
drop table if exists t_subpartition_0012 cascade;
create table t_subpartition_0012(jid int,jn int,name varchar2,unique(jid))partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step8: 创建二级分区表，唯一约束：二级分区键为默认约束名; expect:成功
drop table if exists t_subpartition_0012 cascade;
create table t_subpartition_0012(jid int,jn int,name varchar2,unique(jn))partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step9: 创建二级分区表，唯一约束：一级分区键和二级分区键为默认约束名，第一位是一级分区键; expect:成功
drop table if exists t_subpartition_0012 cascade;
create table t_subpartition_0012(jid int,jn int,name varchar2,unique(jid,jn))partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step10: 创建二级分区表，唯一约束：二级分区键和一级分区键为默认约束名，第一位是二级分区键; expect:成功
drop table if exists t_subpartition_0012 cascade;
create table t_subpartition_0012(jid int,jn int,name varchar2,unique(jn,jid))partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step11: 创建二级分区表，唯一约束：一级分区键和普通列为默认约束名; expect:成功
drop table if exists t_subpartition_0012 cascade;
create table t_subpartition_0012(jid int,jn int,name varchar2,unique(jid,name))partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step12: 创建二级分区表，唯一约束：二级分区键和普通列为默认约束名; expect:成功
drop table if exists t_subpartition_0012 cascade;
create table t_subpartition_0012(jid int,jn int,name varchar2,unique(jn,name))partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step13: 创建二级分区表，唯一约束：一级分区键和二级分区键和普通列为默认约束名; expect:成功
drop table if exists t_subpartition_0012 cascade;
create table t_subpartition_0012(jid int,jn int,name varchar2,unique(jid,jn,name))partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));

--test3: 二级分区键表约束:check约束
--step14: 创建二级分区表，check约束：二级分区键确认约束名; expect:成功
drop table if exists t_subpartition_0012 cascade;
create table t_subpartition_0012(jid int,jn int,name varchar2,constraint hrjpk check(jn>6))partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step15: 创建二级分区表，check约束：二级分区键为默认约束名; expect:成功
drop table if exists t_subpartition_0012 cascade;
create table t_subpartition_0012(jid int,jn int,name varchar2,check(jn>6))partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step16: 创建二级分区表，check约束：二级分区键和一级分区键，第一位是二级分区键; expect:成功
drop table if exists t_subpartition_0012 cascade;
create table t_subpartition_0012(jid int,jn int,name varchar2,check(jn>6 and jid<=8))partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step17: 创建二级分区表，check约束：一级分区键和二级分区键，第一位是一级分区键; expect:成功
drop table if exists t_subpartition_0012 cascade;
create table t_subpartition_0012(jid int,jn int,name varchar2,check(jid>6 and jn<=8))partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step18: 创建二级分区表，check约束：一级分区键和二级分区键和普通列; expect:成功
drop table if exists t_subpartition_0012 cascade;
create table t_subpartition_0012(jid int,jn int,name varchar2,check(jid>6 and jn<=8 and name<>null))partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));

--test4: 二级分区键表约束:外键
--step19: 创建二级分区表，外键：二级分区键确认约束名; expect:成功
drop table if exists t_subpartition_0012 cascade;
drop table if exists t_subpartition_0012_01;
create table if not exists t_subpartition_0012_01(jid int,jn int unique,name varchar2);
create table t_subpartition_0012(jid int,jn int,name varchar2,constraint hrjpk foreign key(jn) references t_subpartition_0012_01(jn))partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step20: 创建二级分区表，外键：二级分区键为默认约束名; expect:成功
drop table if exists t_subpartition_0012 cascade;
drop table if exists t_subpartition_0012_01 cascade;
create table if not exists t_subpartition_0012_01(jid int,jn int unique,name varchar2);
create table t_subpartition_0012(jid int,jn int,name varchar2,foreign key(jn) references t_subpartition_0012_01(jn))partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step21: 创建二级分区表，外键：二级分区键和一级分区键，第一位是二级分区键; expect:成功
drop table if exists t_subpartition_0012 cascade;
drop table if exists t_subpartition_0012_01 cascade;
create table if not exists t_subpartition_0012_01(jid int,jn int,name varchar2,unique(jn,jid));
create table t_subpartition_0012(jid int,jn int,name varchar2,foreign key(jn,jid) references t_subpartition_0012_01(jn,jid))partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step22: 创建二级分区表，外键：一级分区键和二级分区键，第一位是一级分区键; expect:成功
drop table if exists t_subpartition_0012 cascade;
drop table if exists t_subpartition_0012_01 cascade;
create table if not exists t_subpartition_0012_01(jid int,jn int,name varchar2,unique(jn,jid));
create table t_subpartition_0012(jid int,jn int,name varchar2,foreign key(jid,jn) references t_subpartition_0012_01(jn,jid))partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));
--step23: 创建二级分区表，外键：二级分区键和一级分区键和普通列; expect:成功
drop table if exists t_subpartition_0012 cascade;
drop table if exists t_subpartition_0012_01 cascade;
create table if not exists t_subpartition_0012_01(jid int,jn int,name varchar2,unique(jn,jid,name));
create table t_subpartition_0012(jid int,jn int,name varchar2,foreign key(jid,jn,name) references t_subpartition_0012_01(jn,jid,name))partition by hash (jid) subpartition by range(jn)
(partition hr1(subpartition hr11 values less than(6),subpartition hr12 values less than(maxvalue)),partition hr2(subpartition hr21 values less than(6),subpartition hr22 values less than(maxvalue)));

--step24: 删除表; expect:成功
drop table if exists t_subpartition_0012 cascade;
drop table if exists t_subpartition_0012_01 cascade;