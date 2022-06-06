-- @testpoint: 显示当前会话指定的普通表的基本信息，不插入数据

--step1：创建普通表;expect:成功
create table t_temp_0015(
  id integer,
  lb1 text
  );
--step2：查看全局临时表的oid;expect:成功
select oid from pg_class where relname ='t_temp_0015';
--step3: 调用函数显示当前会话指定的全局临时表的基本信息，不插入数据;expect:警告查询无数据
select * from pg_get_gtt_relstats((select oid from pg_class where relname ='t_temp_0015'));
--step4：清理环境;expect:成功
drop table t_temp_0015;