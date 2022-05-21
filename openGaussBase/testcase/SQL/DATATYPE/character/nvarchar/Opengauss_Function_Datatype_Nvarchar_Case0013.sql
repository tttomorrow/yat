-- @testpoint: 行存list分区表-nvarchar(n)的约束\索引\表操作测试 部分测试点合理报错

--step1:建表; expect:成功
drop table if exists t_nvarchar_0013_01 cascade;
drop table if exists t_nvarchar_0013_02 cascade;
create table t_nvarchar_0013_01(c_nvarchar nvarchar primary key);
create table t_nvarchar_0013_02(
c_nvarchar nvarchar
) with (orientation = row) partition by list(c_nvarchar)(
partition p1 values  ('a'),
partition p2 values ('g'),
partition p3 values  ('t'),
partition p4 values  ('u')
);

--step2:约束测试; expect:成功
--增加/删除唯一约束
alter table t_nvarchar_0013_02 add constraint t_nvarchar_0013_02_c_nvarchar_key unique(c_nvarchar);
insert into t_nvarchar_0013_02(c_nvarchar) values('t'),('t');
alter table t_nvarchar_0013_02 drop constraint t_nvarchar_0013_02_c_nvarchar_key;
insert into t_nvarchar_0013_02(c_nvarchar) values('t'),('t');
truncate t_nvarchar_0013_02;
--增加/删除not null约束:支持但null为非法值，合理报错
alter table t_nvarchar_0013_02 modify c_nvarchar not null;
insert into t_nvarchar_0013_02(c_nvarchar) values(null);
alter table t_nvarchar_0013_02 modify c_nvarchar null;
insert into t_nvarchar_0013_02(c_nvarchar) values(null);
truncate t_nvarchar_0013_02;
--增加/删除默认约束
alter table t_nvarchar_0013_02 alter c_nvarchar set default 'a';
insert into t_nvarchar_0013_02(c_nvarchar) values(default);
select c_nvarchar from t_nvarchar_0013_02;
truncate t_nvarchar_0013_02;
alter table t_nvarchar_0013_02 alter c_nvarchar drop default;
insert into t_nvarchar_0013_02(c_nvarchar) values(default);
select c_nvarchar from t_nvarchar_0013_02;
truncate t_nvarchar_0013_02;
--增加/删除检查约束;成功
alter table t_nvarchar_0013_02 add constraint t_nvarchar_0013_02_c_nvarchar_key check (c_nvarchar='t');
insert into t_nvarchar_0013_02(c_nvarchar) values('a');
alter table t_nvarchar_0013_02 drop constraint t_nvarchar_0013_02_c_nvarchar_key;
insert into t_nvarchar_0013_02(c_nvarchar) values('a');
truncate t_nvarchar_0013_02;
--增加/删除主外键约束-成功
alter table t_nvarchar_0013_02 add constraint t_nvarchar_0013_02_c_nvarchar_key  primary key (c_nvarchar);
alter table t_nvarchar_0013_02 add column c_nvarchar1 nvarchar;
alter table t_nvarchar_0013_02 add constraint t_nvarchar_0013_02_c_nvarchar_fkey  foreign key (c_nvarchar1) references t_nvarchar_0013_01(c_nvarchar);
select conname from pg_constraint where conrelid in (select oid from pg_class where relname like 't_nvarchar_0013_02') order by conname;
alter table t_nvarchar_0013_02 drop constraint t_nvarchar_0013_02_c_nvarchar_key cascade;
alter table t_nvarchar_0013_01 drop constraint "t_nvarchar_0013_01_pkey" cascade;
select conname from pg_constraint where conrelid in (select oid from pg_class where relname like 't_nvarchar_0013_02') order by conname;

--step3:索引; expect:成功
create index index_0013_001 on t_nvarchar_0013_02 using btree(c_nvarchar,c_nvarchar1);
--gin索引;expect:成功
create index index_0013_002 on t_nvarchar_0013_02 using gin(to_tsvector('english', c_nvarchar)) local;
--gin索引;expect:失败：error:  global partition index only support btree
create index index_0013_003 on t_nvarchar_0013_02 using gin(to_tsvector('english', c_nvarchar));

--step4:表操作; expect:成功
--增删字段
alter table t_nvarchar_0013_02 drop column c_nvarchar1;
alter table t_nvarchar_0013_02 add column c_nvarchar1 nvarchar;
--修改字段长度
alter table t_nvarchar_0013_02 modify c_nvarchar1 nvarchar(200);
alter table t_nvarchar_0013_02 modify c_nvarchar1 nvarchar(1048576);
alter table t_nvarchar_0013_02 modify c_nvarchar1 nvarchar(1048575);
alter table t_nvarchar_0013_02 modify c_nvarchar1 nvarchar(1048577);
--修改字段类型
alter table t_nvarchar_0013_02 modify c_nvarchar1 nvarchar2(100);
alter table t_nvarchar_0013_02 modify c_nvarchar1 nvarchar(150);
alter table t_nvarchar_0013_02 add constraint t_nvarchar_0013_02_c_nvarchar_key unique(c_nvarchar);
alter table t_nvarchar_0013_02 modify c_nvarchar1 nvarchar2(100);
alter table t_nvarchar_0013_02 modify c_nvarchar1 text;
alter table t_nvarchar_0013_02 modify c_nvarchar1 clob;
alter table t_nvarchar_0013_02 modify c_nvarchar1 char;
alter table t_nvarchar_0013_02 modify c_nvarchar1 nvarchar(150);
--修改分区
--增加分区
alter table t_nvarchar_0013_02 add partition p6 values ('x');
SELECT t1.relname, partstrategy, boundaries
FROM pg_partition t1, pg_class t2
WHERE t1.parentid = t2.oid AND t2.relname = 't_nvarchar_0013_02' AND t1.parttype = 'p' order by t1.relname;
--增加分区
alter table t_nvarchar_0013_02 add partition p5 values ('z');
SELECT t1.relname, partstrategy, boundaries
FROM pg_partition t1, pg_class t2
WHERE t1.parentid = t2.oid AND t2.relname = 't_nvarchar_0013_02' AND t1.parttype = 'p' order by t1.relname;
--删除分区p6;成功
alter table t_nvarchar_0013_02 drop partition for ('x');
SELECT t1.relname, partstrategy, boundaries
FROM pg_partition t1, pg_class t2
WHERE t1.parentid = t2.oid AND t2.relname = 't_nvarchar_0013_02' AND t1.parttype = 'p' order by t1.relname;
--分区p1重命名为p10。
alter table t_nvarchar_0013_02 rename partition p1 to p10;
SELECT t1.relname, partstrategy, boundaries
FROM pg_partition t1, pg_class t2
WHERE t1.parentid = t2.oid AND t2.relname = 't_nvarchar_0013_02' AND t1.parttype = 'p' order by t1.relname;
--分区p2重命名为p11。
alter table t_nvarchar_0013_02 rename partition for ('g') to p11;
SELECT t1.relname, partstrategy, boundaries
FROM pg_partition t1, pg_class t2
WHERE t1.parentid = t2.oid AND t2.relname = 't_nvarchar_0013_02' AND t1.parttype = 'p' order by t1.relname;
--修改分区p1的表空间为example2
drop tablespace if exists tablespace_0013;
create tablespace tablespace_0013 relative location 'tablespace13/tablespace_13';
alter table t_nvarchar_0013_02 move partition p10 tablespace tablespace_0013;
SELECT t1.relname, partstrategy, boundaries
FROM pg_partition t1, pg_class t2
WHERE t1.parentid = t2.oid AND t2.relname = 't_nvarchar_0013_02' AND t1.parttype = 'p' order by t1.relname;
--以t为分割点切分p3;失败：ERROR:  can not split LIST/HASH partition table
alter table t_nvarchar_0013_02 split partition p3 at ('t') into
(
    partition p12,
    partition p13
);
SELECT t1.relname, partstrategy, boundaries
FROM pg_partition t1, pg_class t2
WHERE t1.parentid = t2.oid AND t2.relname = 't_nvarchar_0013_02' AND t1.parttype = 'p' order by t1.relname;
--将p4，p3合并为一个分区;失败：ERROR:  can not merge LIST/HASH partition table
alter table t_nvarchar_0013_02 merge partitions p3, p4 into partition p9;
SELECT t1.relname, partstrategy, boundaries
FROM pg_partition t1, pg_class t2
WHERE t1.parentid = t2.oid AND t2.relname = 't_nvarchar_0013_02' AND t1.parttype = 'p' order by t1.relname;

--step5:sql操作; expect:成功
insert into t_nvarchar_0013_02(c_nvarchar) values ('a'::nvarchar),('g'::nvarchar),('t'::nvarchar),('u'::nvarchar);
select * from t_nvarchar_0013_02 order by c_nvarchar;
update t_nvarchar_0013_02 set c_nvarchar = 'a' where c_nvarchar='z';
select * from t_nvarchar_0013_02 order by c_nvarchar;
delete from t_nvarchar_0013_02 where c_nvarchar = 'g';
select * from t_nvarchar_0013_02 order by c_nvarchar;
select count(*) from t_nvarchar_0013_02 partition (p10);
--upsert;expect:成功
truncate table t_nvarchar_0013_01;
truncate table t_nvarchar_0013_02;
insert into t_nvarchar_0013_02 values ('a','test0013');
select * from t_nvarchar_0013_02 where c_nvarchar = 'a' order by c_nvarchar;
insert into t_nvarchar_0013_02 values ('a','test0013_01') on duplicate key update c_nvarchar1='test0013_01';
select * from t_nvarchar_0013_02 where c_nvarchar = 'a' order by c_nvarchar;

--step6:清理环境; expect:成功
drop table if exists t_nvarchar_0013_01 cascade;
drop table if exists t_nvarchar_0013_02 cascade;
drop tablespace if exists tablespace_0013;