-- @testpoint: 列存range分区表-nvarchar(n)的约束\索引\表操作测试--间隔、hash、list不支持  部分测试点合理报错

--step1:建表; expect:成功
drop table if exists t_nvarchar_0012_01 cascade;
drop table if exists t_nvarchar_0012_02 cascade;
create table t_nvarchar_0012_01(c_nvarchar nvarchar primary key) with(orientation=column);
create table t_nvarchar_0012_02(
c_nvarchar nvarchar
) with (orientation = column) partition by range(c_nvarchar)(
partition p1 values less than ('a'),
partition p2 values less than ('g'),
partition p3 values less than ('k'),
partition p4 values less than ('u')
);

--step2:约束测试; expect:成功
--增加/删除唯一约束
alter table t_nvarchar_0012_02 add constraint t_nvarchar_0012_02_c_nvarchar_key unique(c_nvarchar);
insert into t_nvarchar_0012_02(c_nvarchar) values('test'),('test');
alter table t_nvarchar_0012_02 drop constraint t_nvarchar_0012_02_c_nvarchar_key;
insert into t_nvarchar_0012_02(c_nvarchar) values('test'),('test');
truncate t_nvarchar_0012_02;
--增加/删除not null约束:列存不支持
alter table t_nvarchar_0012_02 modify c_nvarchar not null;
insert into t_nvarchar_0012_02(c_nvarchar) values(null);
alter table t_nvarchar_0012_02 modify c_nvarchar null;
insert into t_nvarchar_0012_02(c_nvarchar) values(null);
truncate t_nvarchar_0012_02;
--增加/删除默认约束
alter table t_nvarchar_0012_02 alter c_nvarchar set default 'test0012';
insert into t_nvarchar_0012_02(c_nvarchar) values(default);
select c_nvarchar from t_nvarchar_0012_02;
truncate t_nvarchar_0012_02;
alter table t_nvarchar_0012_02 alter c_nvarchar drop default;
insert into t_nvarchar_0012_02(c_nvarchar) values(default);
select c_nvarchar from t_nvarchar_0012_02;
truncate t_nvarchar_0012_02;
--增加/删除检查约束;列存不支持
alter table t_nvarchar_0012_02 add constraint t_nvarchar_0012_02_c_nvarchar_key check (c_nvarchar='test');
insert into t_nvarchar_0012_02(c_nvarchar) values('test0012');
alter table t_nvarchar_0012_02 drop constraint t_nvarchar_0012_02_c_nvarchar_key;
insert into t_nvarchar_0012_02(c_nvarchar) values('test0012');
truncate t_nvarchar_0012_02;
--增加/删除主外键约束-列存不支持foreign key
alter table t_nvarchar_0012_02 add constraint t_nvarchar_0012_02_c_nvarchar_key  primary key (c_nvarchar);
alter table t_nvarchar_0012_02 add column c_nvarchar1 nvarchar;
alter table t_nvarchar_0012_02 add constraint t_nvarchar_0012_02_c_nvarchar_fkey  foreign key (c_nvarchar1) references t_nvarchar_0012_01(c_nvarchar);
select conname from pg_constraint where conrelid in (select oid from pg_class where relname like 't_nvarchar_0012_02') order by conname;
alter table t_nvarchar_0012_02 drop constraint t_nvarchar_0012_02_c_nvarchar_key cascade;
alter table t_nvarchar_0012_01 drop constraint "t_nvarchar_0012_01_pkey" cascade;
select conname from pg_constraint where conrelid in (select oid from pg_class where relname like 't_nvarchar_0012_02') order by conname;

--step3:索引; expect:成功
create index index_0012_001 on t_nvarchar_0012_02 using btree(c_nvarchar,c_nvarchar1) local;
--gin索引;expect:成功
create index index_0012_002 on t_nvarchar_0012_02 using gin(to_tsvector('english', c_nvarchar)) local;
--gin索引;expect:失败：error:  global partition index only support btree
create index index_0012_003 on t_nvarchar_0012_02 using gin(to_tsvector('english', c_nvarchar));

--step4:表操作; expect:成功
--增删字段
alter table t_nvarchar_0012_02 drop column c_nvarchar1;
alter table t_nvarchar_0012_02 add column c_nvarchar1 nvarchar;
--修改字段长度
alter table t_nvarchar_0012_02 modify c_nvarchar1 nvarchar(200);
alter table t_nvarchar_0012_02 modify c_nvarchar1 nvarchar(1048576);
alter table t_nvarchar_0012_02 modify c_nvarchar1 nvarchar(1048575);
alter table t_nvarchar_0012_02 modify c_nvarchar1 nvarchar(1048577);
--修改字段类型
alter table t_nvarchar_0012_02 modify c_nvarchar1 nvarchar2(100);
alter table t_nvarchar_0012_02 modify c_nvarchar1 nvarchar(150);
alter table t_nvarchar_0012_02 add constraint t_nvarchar_0012_02_c_nvarchar_key unique(c_nvarchar);
alter table t_nvarchar_0012_02 modify c_nvarchar1 nvarchar2(100);
alter table t_nvarchar_0012_02 modify c_nvarchar1 text;
alter table t_nvarchar_0012_02 modify c_nvarchar1 clob;
alter table t_nvarchar_0012_02 modify c_nvarchar1 char;
alter table t_nvarchar_0012_02 modify c_nvarchar1 nvarchar(150);
--修改分区
--增加分区
alter table t_nvarchar_0012_02 add partition p6 values less than ('x');
SELECT t1.relname, partstrategy, boundaries
FROM pg_partition t1, pg_class t2
WHERE t1.parentid = t2.oid AND t2.relname = 't_nvarchar_0012_02' AND t1.parttype = 'p' order by t1.relname;
--增加分区
alter table t_nvarchar_0012_02 add partition p5 values less than (maxvalue);
SELECT t1.relname, partstrategy, boundaries
FROM pg_partition t1, pg_class t2
WHERE t1.parentid = t2.oid AND t2.relname = 't_nvarchar_0012_02' AND t1.parttype = 'p' order by t1.relname;
--删除分区p6
alter table t_nvarchar_0012_02 drop partition for ('w');
SELECT t1.relname, partstrategy, boundaries
FROM pg_partition t1, pg_class t2
WHERE t1.parentid = t2.oid AND t2.relname = 't_nvarchar_0012_02' AND t1.parttype = 'p' order by t1.relname;
--分区p1重命名为p10。
alter table t_nvarchar_0012_02 rename partition p1 to p10;
SELECT t1.relname, partstrategy, boundaries
FROM pg_partition t1, pg_class t2
WHERE t1.parentid = t2.oid AND t2.relname = 't_nvarchar_0012_02' AND t1.parttype = 'p' order by t1.relname;
--分区p2重命名为p11。
alter table t_nvarchar_0012_02 rename partition for ('f') to p11;
SELECT t1.relname, partstrategy, boundaries
FROM pg_partition t1, pg_class t2
WHERE t1.parentid = t2.oid AND t2.relname = 't_nvarchar_0012_02' AND t1.parttype = 'p' order by t1.relname;
--修改分区p10的表空间为example2
drop tablespace if exists tablespace_0012;
create tablespace tablespace_0012 relative location 'tablespace12/tablespace_12';
alter table t_nvarchar_0012_02 move partition p10 tablespace tablespace_0012;
SELECT t1.relname, partstrategy, boundaries
FROM pg_partition t1, pg_class t2
WHERE t1.parentid = t2.oid AND t2.relname = 't_nvarchar_0012_02' AND t1.parttype = 'p' order by t1.relname;
--以i为分割点切分p3;合理报错
--ERROR:  Un-support feature
--DETAIL:  column-store relation doesn't support this ALTER yet
alter table t_nvarchar_0012_02 split partition p3 at ('i') into
(
    partition p12,
    partition p13
);
SELECT t1.relname, partstrategy, boundaries
FROM pg_partition t1, pg_class t2
WHERE t1.parentid = t2.oid AND t2.relname = 't_nvarchar_0012_02' AND t1.parttype = 'p' order by t1.relname;
--将p3，p4合并为一个分区; expect:成功
alter table t_nvarchar_0012_02 merge partitions p3, p4 into partition p18;
SELECT t1.relname, partstrategy, boundaries
FROM pg_partition t1, pg_class t2
WHERE t1.parentid = t2.oid AND t2.relname = 't_nvarchar_0012_02' AND t1.parttype = 'p' order by t1.relname;

--step5:sql操作; expect:成功
insert into t_nvarchar_0012_02 values ('a'::nvarchar),('b'::nvarchar),('o'::nvarchar),('p'::nvarchar),('x'::nvarchar);
select * from t_nvarchar_0012_02;
update t_nvarchar_0012_02 set c_nvarchar = 'test' where c_nvarchar='1';
select * from t_nvarchar_0012_02;
delete from t_nvarchar_0012_02 where c_nvarchar = '2';
select * from t_nvarchar_0012_02;
select count(*) from t_nvarchar_0012_02 partition (p10);
--upsert;不支持,合理报错
truncate table t_nvarchar_0012_01,t_nvarchar_0012_02;
insert into t_nvarchar_0012_02 values ('a','test0012');
select * from t_nvarchar_0012_02 where c_nvarchar = 'a';
insert into t_nvarchar_0012_02 values ('a','test0012_01') on duplicate key update c_nvarchar1='test0012_01';
select * from t_nvarchar_0012_02 where c_nvarchar = 'a';

--step6:清理环境; expect:成功
drop table if exists t_nvarchar_0012_01 cascade;
drop table if exists t_nvarchar_0012_02 cascade;
drop tablespace if exists tablespace_0012;