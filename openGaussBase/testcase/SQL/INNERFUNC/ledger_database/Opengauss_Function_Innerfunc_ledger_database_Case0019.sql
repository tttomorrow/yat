-- @testpoint: 修复指定防篡改用户表对应的用户历史表hash值，用户表未损坏，进行增删改操作

--step1：建模式建表;expect:成功
drop schema if exists s_ledger_database_0019;
create schema s_ledger_database_0019 with blockchain;
drop table if exists s_ledger_database_0019.t_ledger_database_0019;
create table s_ledger_database_0019.t_ledger_database_0019(id int, name text);
--step2：插入修改删除数据;expect:成功
insert into s_ledger_database_0019.t_ledger_database_0019 values(1, 'alex'), (2, 'bob'), (3, 'peter');
update  s_ledger_database_0019.t_ledger_database_0019 set name = 'bob2' where id = 2;
delete from s_ledger_database_0019.t_ledger_database_0019 where  id = 3;
select pg_catalog.ledger_hist_repair('s_ledger_database_0019', 't_ledger_database_0019');
--step4：清理环境;expect:成功
drop table  s_ledger_database_0019.t_ledger_database_0019;
drop schema s_ledger_database_0019 cascade;