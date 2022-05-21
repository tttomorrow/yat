-- @testpoint: 校验指定防篡改用户的表级数据与hash值与其对应历史表的一致性，不进行增删改操作
--step1：建模式建表;expect:成功
drop schema if exists s_ledger_database_001;
create schema s_ledger_database_001 with blockchain;
drop table if exists s_ledger_database_001.t_ledger_database_001;
create table s_ledger_database_001.t_ledger_database_001(id int, name text);
--step2：调用函数校验指定防篡改用户的表级数据与hash值与其对应历史表的一致性;expect:成功
select pg_catalog.ledger_hist_check('s_ledger_database_001', 't_ledger_database_001');
--step3：清理环境;expect:成功
drop table s_ledger_database_001.t_ledger_database_001;
drop schema s_ledger_database_001 cascade;