-- @testpoint: 验证enable_recyclebin 边界值异常值-1,2-1,1*1,'abc',on*,$on,合理报错

--step1: 查询enable_recyclebin值; expect:显示默认值为off
show enable_recyclebin;

--step2: 修改enable_recyclebin值为-1; expect:修改失败，合理报错
alter system set enable_recyclebin to -1;
select pg_sleep(2);

--step3: 修改enable_recyclebin值为2-1; expect:修改失败，合理报错
alter system set enable_recyclebin to 2-1;
select pg_sleep(2);

--step4: 修改enable_recyclebin值为1*1; expect:修改失败，合理报错
alter system set enable_recyclebin to 1*1;
select pg_sleep(2);

--step5: 修改enable_recyclebin值为'abc'; expect:修改失败，合理报错
alter system set enable_recyclebin to 'abc';
select pg_sleep(2);

--step6: 修改enable_recyclebin值为on*; expect:修改失败，合理报错
alter system set enable_recyclebin to on*;
select pg_sleep(2);

--step7: 修改enable_recyclebin值为$on; expect:修改失败，合理报错
alter system set enable_recyclebin to $on;
select pg_sleep(2);

--step8: 恢复默认值; expect:默认值恢复成功
alter system set enable_recyclebin to off;
select pg_sleep(2);
show enable_recyclebin;