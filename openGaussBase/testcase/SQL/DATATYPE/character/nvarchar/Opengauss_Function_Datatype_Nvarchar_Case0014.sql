-- @testpoint: 行存hash分区表-nvarchar(n)的约束\索引\表操作测试 部分测试点合理报错

--step1:建表; expect:成功
drop table if exists t_nvarchar_0014_01 cascade;
drop table if exists t_nvarchar_0014_02 cascade;
create table t_nvarchar_0014_01(c_nvarchar nvarchar primary key);
create table t_nvarchar_0014_02(
c_nvarchar nvarchar
) with (orientation = row) partition by hash(c_nvarchar)(
partition p1,
partition p2,
partition p3,
partition p4
);

--step2:约束测试; expect:成功
--增加/删除唯一约束
alter table t_nvarchar_0014_02 add constraint t_nvarchar_0014_02_c_nvarchar_key unique(c_nvarchar);
insert into t_nvarchar_0014_02(c_nvarchar) values('t'),('t');
alter table t_nvarchar_0014_02 drop constraint t_nvarchar_0014_02_c_nvarchar_key;
insert into t_nvarchar_0014_02(c_nvarchar) values('t'),('t');
truncate t_nvarchar_0014_02;
--增加/删除not null约束:支持但null为非法值
alter table t_nvarchar_0014_02 modify c_nvarchar not null;
insert into t_nvarchar_0014_02(c_nvarchar) values(null);
alter table t_nvarchar_0014_02 modify c_nvarchar null;
insert into t_nvarchar_0014_02(c_nvarchar) values(null);
truncate t_nvarchar_0014_02;
--增加/删除默认约束
alter table t_nvarchar_0014_02 alter c_nvarchar set default 'a';
insert into t_nvarchar_0014_02(c_nvarchar) values(default);
select c_nvarchar from t_nvarchar_0014_02;
truncate t_nvarchar_0014_02;
alter table t_nvarchar_0014_02 alter c_nvarchar drop default;
insert into t_nvarchar_0014_02(c_nvarchar) values(default);
select c_nvarchar from t_nvarchar_0014_02;
truncate t_nvarchar_0014_02;
--增加/删除检查约束
alter table t_nvarchar_0014_02 add constraint t_nvarchar_0014_02_c_nvarchar_key check (c_nvarchar='t');
insert into t_nvarchar_0014_02(c_nvarchar) values('a');
alter table t_nvarchar_0014_02 drop constraint t_nvarchar_0014_02_c_nvarchar_key;
insert into t_nvarchar_0014_02(c_nvarchar) values('a');
truncate t_nvarchar_0014_02;
--增加/删除主外键约束
alter table t_nvarchar_0014_02 add constraint t_nvarchar_0014_02_c_nvarchar_key  primary key (c_nvarchar);
alter table t_nvarchar_0014_02 add column c_nvarchar1 nvarchar;
alter table t_nvarchar_0014_02 add constraint t_nvarchar_0014_02_c_nvarchar_fkey  foreign key (c_nvarchar1) references t_nvarchar_0014_01(c_nvarchar);
select conname from pg_constraint where conrelid in (select oid from pg_class where relname like 't_nvarchar_0014_02') order by conname;
alter table t_nvarchar_0014_02 drop constraint t_nvarchar_0014_02_c_nvarchar_key cascade;
alter table t_nvarchar_0014_01 drop constraint "t_nvarchar_0014_01_pkey" cascade;
select conname from pg_constraint where conrelid in (select oid from pg_class where relname like 't_nvarchar_0014_02') order by conname;

--step3:索引; expect:成功
create index index_0014_001 on t_nvarchar_0014_02 using btree(c_nvarchar,c_nvarchar1);
--gin索引;expect:成功
create index index_0014_002 on t_nvarchar_0014_02 using gin(to_tsvector('english', c_nvarchar)) local;
--gin索引;expect:失败：error:  global partition index only support btree
create index index_0014_003 on t_nvarchar_0014_02 using gin(to_tsvector('english', c_nvarchar));

--step4:表操作; expect:成功
--增删字段
alter table t_nvarchar_0014_02 drop column c_nvarchar1;
alter table t_nvarchar_0014_02 add column c_nvarchar1 nvarchar;
--修改字段长度
alter table t_nvarchar_0014_02 modify c_nvarchar1 nvarchar(200);
alter table t_nvarchar_0014_02 modify c_nvarchar1 nvarchar(1048576);
alter table t_nvarchar_0014_02 modify c_nvarchar1 nvarchar(1048575);
alter table t_nvarchar_0014_02 modify c_nvarchar1 nvarchar(1048577);
--修改字段类型
alter table t_nvarchar_0014_02 modify c_nvarchar1 nvarchar2(100);
alter table t_nvarchar_0014_02 modify c_nvarchar1 nvarchar(150);
alter table t_nvarchar_0014_02 add constraint t_nvarchar_0014_02_c_nvarchar_key unique(c_nvarchar);
alter table t_nvarchar_0014_02 modify c_nvarchar1 nvarchar2(100);
alter table t_nvarchar_0014_02 modify c_nvarchar1 text;
alter table t_nvarchar_0014_02 modify c_nvarchar1 clob;
alter table t_nvarchar_0014_02 modify c_nvarchar1 char;
alter table t_nvarchar_0014_02 modify c_nvarchar1 nvarchar(150);
--修改分区
--增加/删除分区;
--分区p1重命名为p10。
alter table t_nvarchar_0014_02 rename partition p1 to p10;
SELECT t1.relname, partstrategy, boundaries
FROM pg_partition t1, pg_class t2
WHERE t1.parentid = t2.oid AND t2.relname = 't_nvarchar_0014_02' AND t1.parttype = 'p' order by t1.relname;
--分区'g'重命名为p11。
alter table t_nvarchar_0014_02 rename partition for ('g') to p11;
SELECT t1.relname, partstrategy, boundaries
FROM pg_partition t1, pg_class t2
WHERE t1.parentid = t2.oid AND t2.relname = 't_nvarchar_0014_02' AND t1.parttype = 'p' order by t1.relname;
--修改分区p1的表空间为example2
drop tablespace if exists tablespace_0014;
create tablespace tablespace_0014 relative location 'tablespace14/tablespace_14';
alter table t_nvarchar_0014_02 move partition p11 tablespace tablespace_0014;
SELECT t1.relname, partstrategy, boundaries
FROM pg_partition t1, pg_class t2
WHERE t1.parentid = t2.oid AND t2.relname = 't_nvarchar_0014_02' AND t1.parttype = 'p' order by t1.relname;
--以t为分割点切分p3;失败：ERROR:  can not split LIST/HASH partition table
--将p12，p13合并为一个分区;失败：ERROR:  can not merge LIST/HASH partition table
alter table t_nvarchar_0014_02 split partition p3 at ('t') into
(
    partition p12,
    partition p13
);
SELECT t1.relname, partstrategy, boundaries
FROM pg_partition t1, pg_class t2
WHERE t1.parentid = t2.oid AND t2.relname = 't_nvarchar_0014_02' AND t1.parttype = 'p' order by t1.relname;
--将p4，p3合并为一个分区;失败：ERROR:  can not merge LIST/HASH partition table
alter table t_nvarchar_0014_02 merge partitions p3, p4 into partition p9;
SELECT t1.relname, partstrategy, boundaries
FROM pg_partition t1, pg_class t2
WHERE t1.parentid = t2.oid AND t2.relname = 't_nvarchar_0014_02' AND t1.parttype = 'p' order by t1.relname;

--step5:sql操作; expect:成功
insert into t_nvarchar_0014_02(c_nvarchar) values ('a'::nvarchar),('g'::nvarchar),('t'::nvarchar),('u'::nvarchar),('x'::nvarchar);
select * from t_nvarchar_0014_02;
update t_nvarchar_0014_02 set c_nvarchar = 'a' where c_nvarchar='z';
select * from t_nvarchar_0014_02;
delete from t_nvarchar_0014_02 where c_nvarchar = 'g';
select * from t_nvarchar_0014_02;
select count(*) from t_nvarchar_0014_02 partition (p11);
--upsert;列存不支持
truncate table t_nvarchar_0014_01;
truncate table t_nvarchar_0014_02;
insert into t_nvarchar_0014_02 values ('a','test0014');
select * from t_nvarchar_0014_02 where c_nvarchar = 'a';
insert into t_nvarchar_0014_02 values ('a','test0014_01') on duplicate key update c_nvarchar1='test0014_01';
select * from t_nvarchar_0014_02 where c_nvarchar = 'a';

--step6:清理环境; expect:成功
drop table if exists t_nvarchar_0014_01 cascade;
drop table if exists t_nvarchar_0014_02 cascade;
drop tablespace if exists tablespace_0014;