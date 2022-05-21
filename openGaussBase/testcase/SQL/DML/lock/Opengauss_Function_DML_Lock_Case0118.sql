-- @testpoint: 验证单独SQL for no key update

--step1:建表 插入数据;expect:成功
drop table if exists t_lock_0118_01 cascade;
create table t_lock_0118_01(c_int1 int primary key, c_int2 int);
insert into t_lock_0118_01 values (generate_series(1,20), generate_series(1,20));

--step2:开启事务 执行for no key update;expect:成功
start transaction;
update t_lock_0118_01 set c_int2=21 where c_int1 = 2;
select mode from pg_lock_status() where relation in (select oid from pg_class where relname='t_lock_0118_01');
select mode from pg_locks where relation in (select oid from pg_class where relname='t_lock_0118_01');
commit;
start transaction;
select c_int2 from t_lock_0118_01 where c_int1 = 3 for no key update;
select mode from pg_lock_status() where relation in (select oid from pg_class where relname='t_lock_0118_01');
select mode from pg_locks where relation in (select oid from pg_class where relname='t_lock_0118_01');
commit;

drop table if exists t_lock_0118_02 cascade;
create table t_lock_0118_02(c_int3 int , c_int4 int);
alter table t_lock_0118_02 add foreign key (c_int3) references t_lock_0118_01 (c_int1);
--child里update数据非关联键会获取child的no key update
start transaction;
update t_lock_0118_02 set c_int4=2 where c_int3=1;
select mode from pg_lock_status() where relation in (select oid from pg_class where relname='t_lock_0118_02');
select mode from pg_locks where relation in (select oid from pg_class where relname='t_lock_0118_02');
commit;

--child里insert数据会获取parent的key share
start transaction;
insert into t_lock_0118_02 values(1, 1);
select mode from pg_lock_status() where relation in (select oid from pg_class where relname='t_lock_0118_01');
select mode from pg_locks where relation in (select oid from pg_class where relname='t_lock_0118_01');
commit;

--step3:清理环境;expect:成功
drop table if exists t_lock_0118_01 cascade;
drop table if exists t_lock_0118_02 cascade;