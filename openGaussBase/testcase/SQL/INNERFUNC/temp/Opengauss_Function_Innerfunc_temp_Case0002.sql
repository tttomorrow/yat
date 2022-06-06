-- @testpoint: 显示当前会话指定的全局临时表的基本信息，插入数据

--step1：创建全局临时表只在同一会话中有效;expect:成功
create global temporary table t_temp_002(
  id integer,
  lb1 text
  )on commit preserve rows;
--step2：插入数据;expect:成功
insert into t_temp_002 values(1,'data1');
insert into t_temp_002 values(2,'data2');
--step3：查看全局临时表的oid;expect:成功
select oid from pg_class where relname ='t_temp_002';
--step4: 调用函数显示当前会话指定的全局临时表的基本信息，插入数据;expect:成功
select * from pg_get_gtt_relstats((select oid from pg_class where relname ='t_temp_002'));
--step5：清理环境;expect:成功
drop table t_temp_002;