-- @testpoint: 校验指定防篡改用户表对应的历史表hash与全局历史表对应的relhash一致性，进行增删改操作

--step1：建模式建表;expect:成功
drop schema if exists s_ledger_database_0013;
create schema s_ledger_database_0013 with blockchain;
drop table if exists s_ledger_database_0013.t_ledger_database_0013;
create table s_ledger_database_0013.t_ledger_database_0013(id int, name text);
--step2：插入修改删除数据;expect:成功
insert into s_ledger_database_0013.t_ledger_database_0013 values(1, 'alex'), (2, 'bob'), (3, 'peter');
update  s_ledger_database_0013.t_ledger_database_0013 set name = 'bob2' where id = 2;
delete from s_ledger_database_0013.t_ledger_database_0013 where  id = 3;
--step3：调用函数校验指定防篡改用户表对应的历史表hash与全局历史表对应的relhash一致性;expect:成功
select pg_catalog.ledger_gchain_check('s_ledger_database_0013', 't_ledger_database_0013');
--step4：清理环境;expect:成功
drop table  s_ledger_database_0013.t_ledger_database_0013;
drop schema s_ledger_database_0013 cascade;