-- @testpoint: 对防篡改用户表进行增加操作，将用户历史表归档为1条数据

--step1：建模式，建表
drop schema if exists s_ledger_database_0032;
create schema s_ledger_database_0032 with blockchain;
drop table if exists s_ledger_database_0032.t_ledger_database_0032;
create table s_ledger_database_0032.t_ledger_database_0032(id int, name text);
--step2：插入数据;expect:成功
insert into  s_ledger_database_0032.t_ledger_database_0032 values(1, 'alex'), (2, 'bob'), (3, 'peter');
--step3：调用函对防篡改用户表进行增加操作，将用户历史表归档为1条数据;expect:成功
select pg_catalog.ledger_hist_archive('s_ledger_database_0032', 't_ledger_database_0032');
--step4：查看归档后的结果;expect:成功
select * from blockchain.s_ledger_database_0032_t_ledger_database_0032_hist;
--step5：清理环境;expect:成功
drop table  s_ledger_database_0032.t_ledger_database_0032;
drop schema s_ledger_database_0032 cascade;