-- @testpoint: 修复指定防篡改用户表对应的全局区块表hash值，进行增改操作

--step1：建模式建表;expect:成功
drop schema if exists s_ledger_database_0026;
create schema s_ledger_database_0026 with blockchain;
drop table if exists s_ledger_database_0026.t_ledger_database_0026;
create table s_ledger_database_0026.t_ledger_database_0026(id int, name text);
--step2：插入修改数据;expect:成功
insert into  s_ledger_database_0026.t_ledger_database_0026 values(1, 'alex'), (2, 'bob'), (3, 'peter');
update  s_ledger_database_0026.t_ledger_database_0026 set name = 'bob2' where id = 2;
--step3：调用函数复指定防篡改用户表对应的全局区块表hash值，进行增改操作;expect:返回修复过程中全局区块表hash的增量
select pg_catalog.ledger_gchain_repair('s_ledger_database_0026', 't_ledger_database_0026');
--step4：调用函数校验指定防篡改用户表对应的历史表hash与全局历史表对应的relhash一致性;expect:成功
select pg_catalog.ledger_gchain_check('s_ledger_database_0026', 't_ledger_database_0026');
--step5：清理环境;expect:成功
drop table  s_ledger_database_0026.t_ledger_database_0026;
drop schema s_ledger_database_0026 cascade;