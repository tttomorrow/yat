-- @testpoint: 验证单独SQL for share

--step1:建表 插入数据;expect:成功
drop table if exists t_lock_0117 cascade;
create table t_lock_0117(a int primary key, b int);
insert into t_lock_0117 values (generate_series(1,20), generate_series(1,20));

--step2:开启事务 执行for share;expect:成功
start transaction;
select b from t_lock_0117 where a = 3 for share;
select mode from pg_lock_status() where relation in (select oid from pg_class where relname='t_lock_0117');
select mode from pg_locks where relation in (select oid from pg_class where relname='t_lock_0117');
commit;

--step3:清理环境;expect:成功
drop table if exists t_lock_0117 cascade;