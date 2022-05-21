-- @testpoint: pg_advisory_unlock(key1 int, key2 int)释放会话级别的排它咨询锁
--step1:创建表，插入数据;expect:表创建成功 数据插入成功
drop table if exists tb_pg_advisory_unlock0002;
create table tb_pg_advisory_unlock0002(idnum int primary key, info text);
insert into tb_pg_advisory_unlock0002 values (2,'test');
--step2:更新这条记录的同时，使用一个排它锁，查询数据;expect:加锁成功，表1数据更新成功
start transaction;
select pg_advisory_lock(idnum,idnum) from tb_pg_advisory_unlock0002;
update tb_pg_advisory_unlock0002 set info='mmm' where idnum=2;
select * from tb_pg_advisory_unlock0002 where idnum=2;
--step3:查看当前所有的锁信息;expect:有查到排它型咨询锁
select locktype,mode from pg_locks where locktype = 'advisory' and mode = 'ExclusiveLock';
--step4:释放当前会话所持有的所有咨询锁;expect:释放成功返回t
select pg_advisory_unlock(idnum,idnum) from tb_pg_advisory_unlock0002;
--step5:查看当前所有的锁信息;expect:查询无咨询锁存在
select locktype,mode from pg_locks where locktype = 'advisory' and mode = 'ExclusiveLock';
--step6:提交事务,删除测试表;expect:提交事务，删除成功
end;
drop table tb_pg_advisory_unlock0002;