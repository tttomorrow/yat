-- @testpoint: 显示当前会话指定的本地临时表的单列统计信息

--step1：创建本地临时表只在同一个会话中有效;expect:成功
create local temporary table t_temp_0015(
  id integer,
  lb1 text
  )on commit preserve rows;
--step2：插入数据;expect:成功
insert into t_temp_0015 values(1,'data1');
insert into t_temp_0015 values(2,'data2');
--step3：查看本地临时表的oid;expect:成功
select oid from pg_class where relname ='t_temp_0015';
--step4: 调用函数显示当前会话指定的本地临时表的单列统计信息;expect:警告无查询数据
select * from pg_get_gtt_statistics((select oid from pg_class where relname ='t_temp_0015'),1,''::text);
--step5：清理环境;expect:成功
drop table t_temp_0015;