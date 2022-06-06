-- @testpoint: 校验指定防篡改用户表对应的历史表hash与全局历史表对应的relhash一致性，不进行增删改操作

--step1：建模式建表;expect:成功
drop schema if exists s_ledger_database_0011;
create schema s_ledger_database_0011 with blockchain;
drop table if exists s_ledger_database_0011.t_ledger_database_0011;
create table s_ledger_database_0011.t_ledger_database_0011(id int, name text);
--step2：调用函数校验指定防篡改用户表对应的历史表hash与全局历史表对应的relhash一致性;expect:成功
select pg_catalog.ledger_gchain_check('s_ledger_database_0011', 't_ledger_database_0011');
--step3：清理环境;expect:成功
drop table s_ledger_database_0011.t_ledger_database_0011;
drop schema s_ledger_database_0011 cascade;