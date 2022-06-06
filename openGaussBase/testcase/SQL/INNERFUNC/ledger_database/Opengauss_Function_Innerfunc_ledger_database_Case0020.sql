-- @testpoint: 修复指定防篡改用户表对应的用户历史表hash值，用户表未损坏，参数顺序变换(合理报错）

--step1：建模式建表;expect:成功
drop schema if exists s_ledger_database_0020;
create schema s_ledger_database_0020 with blockchain;
drop table if exists s_ledger_database_0020.t_ledger_database_0020;
create table s_ledger_database_0020.t_ledger_database_0020(id int, name text);
--step2：插入数据;expect:成功
insert into  s_ledger_database_0020.t_ledger_database_0020 values(1, 'alex'), (2, 'bob'), (3, 'peter');
--step3：调用函数修复指定防篡改用户表对应的用户历史表hash值，用户表未损坏，参数顺序变换;expect:失败
select pg_catalog.ledger_hist_repair('t_ledger_database_0020', 's_ledger_database_0020');
--step4：清理环境;expect:成功
drop table  s_ledger_database_0020.t_ledger_database_0020;
drop schema s_ledger_database_0020 cascade;