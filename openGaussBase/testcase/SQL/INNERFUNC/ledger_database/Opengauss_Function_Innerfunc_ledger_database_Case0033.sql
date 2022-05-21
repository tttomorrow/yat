-- @testpoint: 对防篡改用户表进行增加删除操作，将用户历史表归档为1条数据

--step1：建模式，建表
drop schema if exists s_ledger_database_0033;
create schema s_ledger_database_0033 with blockchain;
drop table if exists s_ledger_database_0033.t_ledger_database_0033;
create table s_ledger_database_0033.t_ledger_database_0033(id int, name text);
--step2：插入删除数据;expect:成功
insert into  s_ledger_database_0033.t_ledger_database_0033 values(1, 'alex'), (2, 'bob'), (3, 'peter');
delete from s_ledger_database_0033.t_ledger_database_0033 where id = 3;
--step3：调用函对防篡改用户表进行增加删除操作，将用户历史表归档为1条数据;expect:成功
select pg_catalog.ledger_hist_archive('s_ledger_database_0033', 't_ledger_database_0033');
--step4：查看归档后的结果;expect:成功
select * from blockchain.s_ledger_database_0033_t_ledger_database_0033_hist;
--step5：清理环境;expect:成功
drop table  s_ledger_database_0033.t_ledger_database_0033;
drop schema s_ledger_database_0033 cascade;