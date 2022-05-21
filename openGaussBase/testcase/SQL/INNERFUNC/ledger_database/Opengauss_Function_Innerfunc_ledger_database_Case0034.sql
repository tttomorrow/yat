-- @testpoint: 对防篡改用户表进行增加修改操作，将用户历史表归档为1条数据

--step1：建模式，建表
drop schema if exists s_ledger_database_0034;
create schema s_ledger_database_0034 with blockchain;
drop table if exists s_ledger_database_0034.t_ledger_database_0034;
create table s_ledger_database_0034.t_ledger_database_0034(id int, name text);
--step2：插入修改数据;expect:成功
insert into  s_ledger_database_0034.t_ledger_database_0034 values(1, 'alex'), (2, 'bob'), (3, 'peter');
update s_ledger_database_0034.t_ledger_database_0034 set name = 'alext' where id = 1;
--step3：调用函对防篡改用户表进行增加修改操作，将用户历史表归档为1条数据;expect:成功
select pg_catalog.ledger_hist_archive('s_ledger_database_0034', 't_ledger_database_0034');
--step4：查看归档后的结果;expect:成功
select * from blockchain.s_ledger_database_0034_t_ledger_database_0034_hist;
--step5：清理环境;expect:成功
drop table  s_ledger_database_0034.t_ledger_database_0034;
drop schema s_ledger_database_0034 cascade;