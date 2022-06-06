-- @testpoint: 列存本地临时表-nvarchar(n)的约束\索引\表操作测试 部分测试点合理报错

--step1:建表; expect:成功
drop table if exists t_nvarchar_0010_01 cascade;
drop table if exists t_nvarchar_0010_02 cascade;
create temporary table t_nvarchar_0010_01(c_nvarchar nvarchar primary key)  with(orientation=column);
create temporary table t_nvarchar_0010_02(c_nvarchar nvarchar)  with(orientation=column);

--step2:约束测试; expect:成功
--增加/删除唯一约束
alter table t_nvarchar_0010_02 add constraint t_nvarchar_0010_02_c_nvarchar_key unique(c_nvarchar);
insert into t_nvarchar_0010_02(c_nvarchar) values('test'),('test');
alter table t_nvarchar_0010_02 drop constraint t_nvarchar_0010_02_c_nvarchar_key;
insert into t_nvarchar_0010_02(c_nvarchar) values('test'),('test');
truncate t_nvarchar_0010_02;
--增加/删除not null约束:列存不支持
alter table t_nvarchar_0010_02 modify c_nvarchar not null;
insert into t_nvarchar_0010_02(c_nvarchar) values(null);
alter table t_nvarchar_0010_02 modify c_nvarchar null;
insert into t_nvarchar_0010_02(c_nvarchar) values(null);
truncate t_nvarchar_0010_02;
--增加/删除默认约束
alter table t_nvarchar_0010_02 alter c_nvarchar set default 'test0010';
insert into t_nvarchar_0010_02(c_nvarchar) values(default);
select c_nvarchar from t_nvarchar_0010_02;
truncate t_nvarchar_0010_02;
alter table t_nvarchar_0010_02 alter c_nvarchar drop default;
insert into t_nvarchar_0010_02(c_nvarchar) values(default);
select c_nvarchar from t_nvarchar_0010_02;
truncate t_nvarchar_0010_02;
--增加/删除检查约束;列存不支持
alter table t_nvarchar_0010_02 add constraint t_nvarchar_0010_02_c_nvarchar_key check (c_nvarchar='test');
insert into t_nvarchar_0010_02(c_nvarchar) values('test0010');
alter table t_nvarchar_0010_02 drop constraint t_nvarchar_0010_02_c_nvarchar_key;
insert into t_nvarchar_0010_02(c_nvarchar) values('test0010');
truncate t_nvarchar_0010_02;
--增加/删除主外键约束-列存不支持foreign key
alter table t_nvarchar_0010_02 add constraint t_nvarchar_0010_02_c_nvarchar_key  primary key (c_nvarchar);
alter table t_nvarchar_0010_02 add column c_nvarchar1 nvarchar;
alter table t_nvarchar_0010_02 add constraint t_nvarchar_0010_02_c_nvarchar_fkey  foreign key (c_nvarchar1) references t_nvarchar_0010_01(c_nvarchar);
select conname from pg_constraint where conrelid in (select oid from pg_class where relname like 't_nvarchar_0010_02') order by conname;
alter table t_nvarchar_0010_02 drop constraint t_nvarchar_0010_02_c_nvarchar_key cascade;
alter table t_nvarchar_0010_01 drop constraint "t_nvarchar_0010_01_pkey" cascade;
alter table t_nvarchar_0010_02 drop constraint t_nvarchar_0010_02_c_nvarchar_fkey cascade;
select conname from pg_constraint where conrelid in (select oid from pg_class where relname like 't_nvarchar_0010_02') order by conname;

--step3:索引; expect:成功
create index index_0010_001 on t_nvarchar_0010_02(c_nvarchar,c_nvarchar1);
--gin索引;expect:成功
create index index_0010_002 on t_nvarchar_0010_02 using gin(to_tsvector('english', c_nvarchar));


--step4:表操作; expect:成功
--增删字段
alter table t_nvarchar_0010_02 drop column c_nvarchar1;
alter table t_nvarchar_0010_02 add column c_nvarchar1 nvarchar;
--修改字段长度
alter table t_nvarchar_0010_02 modify c_nvarchar1 nvarchar(200);
alter table t_nvarchar_0010_02 modify c_nvarchar1 nvarchar(1048576);
alter table t_nvarchar_0010_02 modify c_nvarchar1 nvarchar(1048575);
alter table t_nvarchar_0010_02 modify c_nvarchar1 nvarchar(1048577);
--修改字段类型
alter table t_nvarchar_0010_02 modify c_nvarchar1 nvarchar2(100);
alter table t_nvarchar_0010_02 modify c_nvarchar1 nvarchar(150);
alter table t_nvarchar_0010_02 add constraint t_nvarchar_0010_02_c_nvarchar_key unique(c_nvarchar);
alter table t_nvarchar_0010_02 modify c_nvarchar1 nvarchar2(100);
alter table t_nvarchar_0010_02 modify c_nvarchar1 text;
alter table t_nvarchar_0010_02 modify c_nvarchar1 clob;
alter table t_nvarchar_0010_02 modify c_nvarchar1 char;
alter table t_nvarchar_0010_02 modify c_nvarchar1 nvarchar(150);

--step5:sql操作; expect:成功
insert into t_nvarchar_0010_02 values (1::nvarchar),(2::nvarchar),(3::nvarchar),(4::nvarchar),(5::nvarchar);
select * from t_nvarchar_0010_02;
update t_nvarchar_0010_02 set c_nvarchar = 'test' where c_nvarchar='1';
select * from t_nvarchar_0010_02;
delete from t_nvarchar_0010_02 where c_nvarchar = '2';
select * from t_nvarchar_0010_02;
--upsert;列存不支持
truncate t_nvarchar_0010_01;
truncate t_nvarchar_0010_02;
insert into t_nvarchar_0010_02 values ('a','test0010');
select * from t_nvarchar_0010_02 where c_nvarchar = 'a';
insert into t_nvarchar_0010_02 values ('a','test0010_01') on duplicate key update c_nvarchar1='test0010_01';
select * from t_nvarchar_0010_02 where c_nvarchar = 'a';

--step6:清理环境; expect:成功
drop table if exists t_nvarchar_0010_01 cascade;
drop table if exists t_nvarchar_0010_02 cascade;
