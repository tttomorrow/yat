-- @testpoint: pg_advisory_unlock_shared(key bigint)释放会话级别的共享咨询锁
--step1:创建表，使用一个唯一num（用于advisory lock），插入数据;expect:表创建成功 数据插入成功
drop table if exists tb_advisorylock_aus_0001;
create table tb_advisorylock_aus_0001(num int8 primary key, name text);
insert into tb_advisorylock_aus_0001 values (2,'test');
--step2:使用pg_advisory_lock_shared函数加锁更新数据；查询数据;expect:加锁成功，数据更新成功
start transaction;
select pg_advisory_lock_shared(num) from tb_advisorylock_aus_0001;
update tb_advisorylock_aus_0001 set name='bbb' where num=2;
--step3:查看当前所有的锁信息;expect:查询到一个共享咨询锁
select locktype,mode  from pg_locks where locktype = 'advisory' and mode = 'ShareLock';
--step4:释放当前会话所持有的所有咨询锁;expect:解锁成功
select pg_advisory_unlock_shared(num) from tb_advisorylock_aus_0001;
--step5:查看当前所有的锁信息;expect:查无共享咨询锁
select locktype,mode from pg_locks where locktype = 'advisory' and mode = 'ShareLock';
--step6:提交事务;删除测试表;expect:提交成功;删除成功
commit;
drop table if exists tb_advisorylock_aus_0001;