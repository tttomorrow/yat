-- @testpoint: 在非篡改模式下修复指定防篡改用户表对应的全局区块表hash值，不进行操作（合理报错）


--step1：建模式建表;expect:成功
drop schema if exists s_ledger_database_0038;
create schema s_ledger_database_0038;
drop table if exists s_ledger_database_0038.t_ledger_database_0038;
create table s_ledger_database_0038.t_ledger_database_0038(id int, name text);
--step2：调用函数在非篡改模式下修复指定防篡改用户表对应的全局区块表hash值，不进行操作;expect:失败
select pg_catalog.ledger_gchain_repair('s_ledger_database_0038', 't_ledger_database_0038');
--step3：清理环境;expect:成功
drop table  s_ledger_database_0038.t_ledger_database_0038;
drop schema s_ledger_database_0038 cascade;