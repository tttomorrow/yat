-- @testpoint: pg_stat_get_wlm_session_info(int flag),获取当前内存中记录的TopSQL查询语句级别相关统计信息，入参为无效值（为空、特殊字符、多参）时，合理报错

----step1：开启资源管理功能; expect:成功
alter system set use_workload_manager to on;

----step2：参数生效略有延迟，等待始参数生效; expect:成功
select pg_sleep(3);

----step3：入参为空; expect:合理报错
select pg_stat_get_wlm_session_info();

----step4：入参为特殊字符; expect:合理报
select pg_stat_get_wlm_session_info('@%');

----step5：多参; expect:合理报错
select pg_stat_get_wlm_session_info(1,2);

----step6：关闭资源管理功能; expect:成功
alter system set use_workload_manager to off;

----step7：参数生效略有延迟，等待始参数生效; expect:成功
select pg_sleep(5);