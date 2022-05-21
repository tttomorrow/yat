-- @testpoint: 非篡改模式校验指定防篡改用户表对应的历史表hash与全局历史表对应的relhash一致性，进行增改操作（合理报错）

--step1：建模式建表;expect:成功
drop schema if exists s_ledger_database_0044;
create schema s_ledger_database_0044;
drop table if exists s_ledger_database_0044.t_ledger_database_0044;
create table s_ledger_database_0044.t_ledger_database_0044(id int, name text);
--step2：插入修改数据;expect:成功
insert into s_ledger_database_0044.t_ledger_database_0044 values(1, 'alex'), (2, 'bob'), (3, 'peter');
update  s_ledger_database_0044.t_ledger_database_0044 set name = 'bob2' where id = 2;
--step3：非篡改模式调用函数校验指定防篡改用户表对应的历史表hash与全局历史表对应的relhash一致性;expect:失败
select pg_catalog.ledger_gchain_check('s_ledger_database_0044', 't_ledger_database_0044');
--step4：清理环境;expect:成功
drop table  s_ledger_database_0044.t_ledger_database_0044;
drop schema s_ledger_database_0044 cascade;