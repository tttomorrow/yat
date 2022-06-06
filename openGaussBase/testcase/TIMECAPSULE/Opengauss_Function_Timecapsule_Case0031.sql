-- @testpoint: 不支持闪回drop,truncate unlogged表,合理报错

--step1: 查询enable_recyclebin 默认值; expect:显示默认值
show enable_recyclebin;

--step2: 修改enable_recyclebin为off; expect:显示值为off
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 清空回收站; expect:回收站清空成功
drop table if exists t_timecapsule_0031;
purge recyclebin;

--step4: 创建unlogged表; expect:表创建成功
create unlogged table t_timecapsule_0031
(
    w_warehouse_sk            integer               not null,
    w_warehouse_id            char(16)              not null,
    w_warehouse_name          varchar(20)                   ,
    w_warehouse_sq_ft         integer                       ,
    w_street_number           char(10)                      ,
    w_street_name             varchar(60)                   ,
    w_street_type             char(15)                      ,
    w_suite_number            char(10)                      ,
    w_city                    varchar(60)                   ,
    w_county                  varchar(30)                   ,
    w_state                   char(2)                       ,
    w_zip                     char(10)                      ,
    w_country                 varchar(20)                   ,
    w_gmt_offset              decimal(5,2)
);

--step5: 清空表数据; expect:表数据清空成功
truncate table t_timecapsule_0031;

--step6: 执行truncate闪回; expect:闪回失败，合理报错
timecapsule table t_timecapsule_0031 to before truncate;

--step7: 删除表; expect:表删除成功
drop table t_timecapsule_0031;

--step8: 执行drop闪回; expect:闪回失败，合理报错
timecapsule table t_timecapsule_0031 to before drop;

--step9: 清理环境; expect:清理成功
drop table if exists t_timecapsule_0031 purge;
purge recyclebin;

--step10: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;