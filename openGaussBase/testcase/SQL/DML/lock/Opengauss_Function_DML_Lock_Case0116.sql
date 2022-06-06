-- @testpoint: 验证单独SQL for update

--step1:建表 插入数据;expect:成功
drop table if exists t_lock_0116 cascade;
create table t_lock_0116(a int primary key, b int);
insert into t_lock_0116 values (generate_series(1,20), generate_series(1,20));

--step2:开启事务 执行for update;expect:成功
start transaction;
delete from t_lock_0116 where a = 1;
select mode from pg_lock_status() where relation in (select oid from pg_class where relname='t_lock_0116');
select mode from pg_locks where relation in (select oid from pg_class where relname='t_lock_0116');
commit;
start transaction;
update t_lock_0116 set a=21 where a = 2;
select mode from pg_lock_status() where relation in (select oid from pg_class where relname='t_lock_0116');
select mode from pg_locks where relation in (select oid from pg_class where relname='t_lock_0116');
commit;
start transaction;
select b from t_lock_0116 where a = 3 for update;
select mode from pg_lock_status() where relation in (select oid from pg_class where relname='t_lock_0116');
select mode from pg_locks where relation in (select oid from pg_class where relname='t_lock_0116');
commit;

select * from t_lock_0116 where a in (1,2,3,21);

--step3:清理环境;expect:成功
drop table if exists t_lock_0116 cascade;