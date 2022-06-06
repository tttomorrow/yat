-- @testpoint: 修复指定防篡改用户表对应的用户历史表hash值，用户历史表未损坏，不进行增删改操作
--step1：建模式建表;expect:成功
drop schema if exists s_ledger_database_0017;
create schema s_ledger_database_0017 with blockchain;
drop table if exists s_ledger_database_0017.t_ledger_database_0017;
create table s_ledger_database_0017.t_ledger_database_0017(id int, name text);
select pg_catalog.ledger_hist_repair('s_ledger_database_0017', 't_ledger_database_0017');
--step3：清理环境;expect:成功
drop table s_ledger_database_0017.t_ledger_database_0017;
drop schema s_ledger_database_0017 cascade;