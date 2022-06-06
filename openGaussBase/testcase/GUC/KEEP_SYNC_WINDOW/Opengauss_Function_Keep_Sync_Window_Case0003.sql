-- @testpoint: 使用alter system set方法设置参数为0 ,2147483647,10,1min
--step1:查询默认值;expect:默认值为0
show keep_sync_window;
--step2:修改参数值为0;expect:修改成功
alter system set keep_sync_window to 0;
select pg_sleep(2);
--step3:查询修改后的查询值;expect:值为0
show keep_sync_window;
--step4:修改参数值为2147483647;expect:修改成功
alter system set keep_sync_window to 2147483647;
select pg_sleep(2);
--step5:查询修改后的查询值;expect:值为2147483647s
show keep_sync_window;
--step6:修改参数值为10;expect:修改成功
alter system set keep_sync_window to 10;
select pg_sleep(2);
--step7:查询修改后的查询值;expect:值为10s
show keep_sync_window;
--step8:修改参数值为1min;expect:修改成功
alter system set keep_sync_window to "1min";
select pg_sleep(2);
--step9:查询修改后的查询值;expect:值为1min
show keep_sync_window;
--step10:恢复默认值;expect:默认值恢复成功
alter system set keep_sync_window to 0;
select pg_sleep(2);
show keep_sync_window;