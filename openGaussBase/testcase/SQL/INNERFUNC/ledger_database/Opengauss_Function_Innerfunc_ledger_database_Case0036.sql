-- @testpoint: 在非篡改模式下对防篡改用户表不进行操作，将用户历史表归档为1条数据（合理报错）

--step1：建模式（非篡改模式），建表
drop schema if exists s_ledger_database_0036;
create schema s_ledger_database_0036;
drop table if exists s_ledger_database_0036.t_ledger_database_0036;
create table s_ledger_database_0036.t_ledger_database_0036(id int, name text);
--step2：调用函数在非篡改模式下对防篡改用户表不进行操作，将用户历史表归档为1条数据;expect:失败
select pg_catalog.ledger_hist_archive('s_ledger_database_0036', 't_ledger_database_0036');
--step3：清理环境;expect:成功
drop table  s_ledger_database_0036.t_ledger_database_0036;
drop schema s_ledger_database_0036 cascade;