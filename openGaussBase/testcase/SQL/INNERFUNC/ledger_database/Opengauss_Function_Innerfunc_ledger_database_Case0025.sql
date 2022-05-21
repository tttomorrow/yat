-- @testpoint: 修复指定防篡改用户表对应的全局区块表hash值，区块表未损坏，不进行增删改操作
--step1：建模式建表;expect:成功
drop schema if exists s_ledger_database_0025;
create schema s_ledger_database_0025 with blockchain;
drop table if exists s_ledger_database_0025.t_ledger_database_0025;
create table s_ledger_database_0025.t_ledger_database_0025(id int, name text);
select pg_catalog.ledger_gchain_repair('s_ledger_database_0025', 't_ledger_database_0025');
--step3：清理环境;expect:成功
drop table s_ledger_database_0025.t_ledger_database_0025;
drop schema s_ledger_database_0025 cascade;