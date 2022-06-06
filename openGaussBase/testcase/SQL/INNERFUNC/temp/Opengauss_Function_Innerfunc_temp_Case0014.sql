-- @testpoint: 显示当前会话指定的本地临时表的基本信息，不插入数据

--step1：创建全局临时表只在同一会话中有效;expect:成功
create local temporary table t_temp_0014(
  id integer,
  lb1 text
  )on commit preserve rows;
--step2：查看全局临时表的oid;expect:成功
select oid from pg_class where relname ='t_temp_0014';
--step3: 调用函数显示当前会话指定的全局临时表的基本信息，不插入数据;expect:警告查询无数据
select * from pg_get_gtt_relstats((select oid from pg_class where relname ='t_temp_0014'));
--step4：清理环境;expect:成功
drop table t_temp_0014;