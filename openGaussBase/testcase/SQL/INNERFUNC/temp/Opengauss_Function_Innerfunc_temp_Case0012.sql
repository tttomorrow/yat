-- @testpoint: 显示正在使用指定本地临时表的所有线程pid（合理报错）

--step1：创建本地临时表只在同一个会话中有效;expect:成功
create local temporary table t_temp_0012(
  id integer,
  lb1 text
  )on commit preserve rows;
--step2：插入数据;expect:成功
insert into t_temp_0012 values(1,'data1');
insert into t_temp_0012 values(2,'data2');
--step3：查看本地临时表的oid;expect:成功
select oid from pg_class where relname ='t_temp_0012';
--step4: 调用函数显示正在使用指定本地临时表的所有线程pid;expect:发出警告查询无数据
select * from pg_gtt_attached_pid((select oid from pg_class where relname ='t_temp_0012'));
--step5：清理环境;expect:成功
drop table t_temp_0012;