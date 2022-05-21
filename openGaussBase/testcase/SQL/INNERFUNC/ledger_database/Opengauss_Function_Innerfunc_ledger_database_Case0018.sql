-- @testpoint: 修复指定防篡改用户表对应的用户历史表hash值，用户表未损坏，进行增改操作

--step1：建模式建表;expect:成功
drop schema if exists s_ledger_database_0018;
create schema s_ledger_database_0018 with blockchain;
drop table if exists s_ledger_database_0018.t_ledger_database_0018;
create table s_ledger_database_0018.t_ledger_database_0018(id int, name text);
--step2：插入修改数据;expect:成功
insert into  s_ledger_database_0018.t_ledger_database_0018 values(1, 'alex'), (2, 'bob'), (3, 'peter');
update  s_ledger_database_0018.t_ledger_database_0018 set name = 'bob2' where id = 2;
select pg_catalog.ledger_hist_repair('s_ledger_database_0018', 't_ledger_database_0018');
--step4：清理环境;expect:成功
drop table  s_ledger_database_0018.t_ledger_database_0018;
drop schema s_ledger_database_0018 cascade;