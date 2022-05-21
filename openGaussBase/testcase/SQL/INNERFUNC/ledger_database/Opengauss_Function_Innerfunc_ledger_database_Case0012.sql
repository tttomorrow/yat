-- @testpoint: 校验指定防篡改用户表对应的历史表hash与全局历史表对应的relhash一致性，进行增改操作

--step1：建模式建表;expect:成功
drop schema if exists s_ledger_database_0012;
create schema s_ledger_database_0012 with blockchain;
drop table if exists s_ledger_database_0012.t_ledger_database_0012;
create table s_ledger_database_0012.t_ledger_database_0012(id int, name text);
--step2：插入修改数据;expect:成功
insert into s_ledger_database_0012.t_ledger_database_0012 values(1, 'alex'), (2, 'bob'), (3, 'peter');
update  s_ledger_database_0012.t_ledger_database_0012 set name = 'bob2' where id = 2;
--step3：调用函数校验指定防篡改用户表对应的历史表hash与全局历史表对应的relhash一致性;expect:一致则返回t
select pg_catalog.ledger_gchain_check('s_ledger_database_0012', 't_ledger_database_0012');
--step4：清理环境;expect:成功
drop table  s_ledger_database_0012.t_ledger_database_0012;
drop schema s_ledger_database_0012 cascade;