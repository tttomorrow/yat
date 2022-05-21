-- @testpoint: pg_advisory_unlock_all()释放当前会话持有的所有咨询锁
--step1:创建表，插入数据;expect:建表成功
drop table if exists tb_aua_case0001;
create table tb_aua_case0001(id int4 primary key, info text);
insert into tb_aua_case0001 values (2,'test');
--step2:使用advisory lock锁住这个ID，
select pg_advisory_lock_shared(id, id) from tb_aua_case0001;
--step3:查看当前所有的锁信息;expect:有查到存在的咨询锁
select locktype,mode from pg_locks where locktype = 'advisory';
--step4:释放当前会话所持有的所有咨询锁;expect:执行成功,返回void
select pg_advisory_unlock_all();
--step5:查看当前所有的锁信息;expect:查询无咨询锁存在
select locktype,mode from pg_locks where locktype = 'advisory';
--step6:删除测试表;expect:删除成功
drop table tb_aua_case0001;