-- @testpoint: pg_stat_set_last_data_changed_time(oid),手动设置该表上最后一次操作的时间,函数的异常校验，合理报错

----step1：创建表; expect:成功
create table tb_statistics_function_case0160(id int);
----step1：入参为空; expect:合理报错
select pg_stat_set_last_data_changed_time() from PG_CLASS a where a.relname = 'tb_statistics_function_case0160';

----step2：多参; expect:合理报错
select pg_stat_set_last_data_changed_time(a.oid,a.oid,a.oid) from PG_CLASS a where a.relname = 'tb_statistics_function_case0160';

----step3：入参超范围; expect:合理报错
select pg_stat_set_last_data_changed_time(9999999999999) from PG_CLASS a where a.relname = 'tb_statistics_function_case0160';

----step4：入参为特殊字符; expect:合理报错
select pg_stat_set_last_data_changed_time('**&&^') from PG_CLASS a where a.relname = 'tb_statistics_function_case0160';

----step5：清理环境; expect:成功
drop table tb_statistics_function_case0160;