-- @testpoint: 在非篡改模式下对防篡改用户表进行增加修改操作，将用户历史表归档为1条数据（合理报错）

--step1：建模式（非篡改模式），建表
drop schema if exists s_ledger_database_0035;
create schema s_ledger_database_0035;
drop table if exists s_ledger_database_0035.t_ledger_database_0035;
create table s_ledger_database_0035.t_ledger_database_0035(id int, name text);
--step2：插入修改数据;expect:成功
insert into  s_ledger_database_0035.t_ledger_database_0035 values(1, 'alex'), (2, 'bob'), (3, 'peter');
update s_ledger_database_0035.t_ledger_database_0035 set name = 'alext' where id = 1;
--step3：调用函数在非篡改模式下对防篡改用户表进行增加修改操作，将用户历史表归档为1条数据;expect:失败
select pg_catalog.ledger_hist_archive('s_ledger_database_0035', 't_ledger_database_0035');
--step4：清理环境;expect:成功
drop table  s_ledger_database_0035.t_ledger_database_0035;
drop schema s_ledger_database_0035 cascade;