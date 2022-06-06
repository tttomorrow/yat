-- @testpoint: 在非篡改模式下修复指定防篡改用户表对应的用户历史表hash值，不进行操作（合理报错）

--step1：建模式建表;expect:成功
drop schema if exists s_ledger_database_0040;
create schema s_ledger_database_0040;
drop table if exists s_ledger_database_0040.t_ledger_database_0040;
create table s_ledger_database_0040.t_ledger_database_0040(id int, name text);
--step2：调用函数在非篡改模式下修复指定防篡改用户表对应的用户历史表hash值，不进行操作;expect:失败
select pg_catalog.ledger_hist_repair('s_ledger_database_0040','t_ledger_database_0040');
--step3：删除表;expect:成功
drop table s_ledger_database_0040.t_ledger_database_0040;
drop schema s_ledger_database_0040 cascade;