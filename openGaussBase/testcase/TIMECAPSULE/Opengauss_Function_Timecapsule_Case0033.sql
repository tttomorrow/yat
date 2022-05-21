-- @testpoint: 闪回drop,truncate 带外键的表

--step1: 查询enable_recyclebin 默认值; expect:显示默认值
show enable_recyclebin;

--step2: 修改enable_recyclebin为on; expect:修改成功
alter system set enable_recyclebin to on;
select pg_sleep(2);
show enable_recyclebin;

--step3: 如果表存在清除表且清除回收站; expect:表清除成功且回收站清除成功
drop table if exists t_timecapsule_0033_01;
drop table if exists t_timecapsule_0033_02;
purge recyclebin;

--step4: 创建表; expect:表创建成功
create table t_timecapsule_0033_01
(
    w_city            varchar(60)                primary key,
    w_address       text
);

create table t_timecapsule_0033_02
(
    w_warehouse_sk            integer               not null,
    w_warehouse_id            char(16)              not null,
    w_warehouse_name          varchar(20)                   ,
    w_warehouse_sq_ft         integer                       ,
    w_street_number           char(10)                      ,
    w_street_name             varchar(60)                   ,
    w_street_type             char(15)                      ,
    w_suite_number            char(10)                      ,
    w_city                    varchar(60)           references t_timecapsule_0033_01(w_city),
    w_county                  varchar(30)                   ,
    w_state                   char(2)                       ,
    w_zip                     char(10)                      ,
    w_country                 varchar(20)                   ,
    w_gmt_offset              decimal(5,2)
);

--step5: 清空表; expect:表清空成功
truncate table t_timecapsule_0033_02;

--step6: 对外键表执行闪回truncate; expect:闪回成功
timecapsule table t_timecapsule_0033_02 to before truncate;

--step7: 查询闪回的外键表; expect:查询结果为空与预期结果一致
select * from t_timecapsule_0033_02;

--step8: 删除表; expect:表删除成功
drop table t_timecapsule_0033_02;

--step9: 对外键表执行闪回drop; expect:闪回成功
timecapsule table t_timecapsule_0033_02 to before drop;

--step10: 查询闪回的外键表; expect:查询结果为空与预期结果一致
select * from t_timecapsule_0033_02;

--step11: 清理环境; expect:清理成功
drop table if exists t_timecapsule_0033_02 purge;
drop table if exists t_timecapsule_0033_01 purge;
purge recyclebin;

--step12: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;