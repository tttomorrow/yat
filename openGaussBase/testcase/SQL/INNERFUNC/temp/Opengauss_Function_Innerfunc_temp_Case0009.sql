-- @testpoint: 显示正在使用指定全局临时表的所有线程pid

--step1：创建全局临时表只在同一会话中有效;expect:成功
create global temporary table t_temp_009(
  id integer,
  lb1 text
  )on commit preserve rows;
--step2：插入数据;expect:成功
insert into t_temp_009 values(1,'data1');
insert into t_temp_009 values(2,'data2');
--step3：查看全局临时表的oid;expect:成功
select oid from pg_class where relname ='t_temp_009';
--step4: 调用函数显示正在使用指定全局临时表的所有线程pid;expect:成功
select * from pg_gtt_attached_pid((select oid from pg_class where relname ='t_temp_009'));
--step5：清理环境;expect:成功
drop table t_temp_009;