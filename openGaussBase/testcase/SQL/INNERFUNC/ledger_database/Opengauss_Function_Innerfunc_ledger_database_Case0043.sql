-- @testpoint: 在非篡改模式下校验防篡改用户表对应的历史表hash与全局历史表的relhash一致性，不进行增删改操作（合理报错）

--step1：建模式建表;expect:成功
drop schema if exists s_ledger_database_0043;
create schema s_ledger_database_0043;
drop table if exists s_ledger_database_0043.t_ledger_database_0043;
create table s_ledger_database_0043.t_ledger_database_0043(id int, name text);
--step2：调用函数在非篡改模式下校验防篡改用户表对应的历史表hash与全局历史表对应的relhash一致性，不进行操作;expect:失败
select pg_catalog.ledger_gchain_check('s_ledger_database_0043', 't_ledger_database_0043');
--step3：清理环境;expect:成功
drop table s_ledger_database_0043.t_ledger_database_0043;
drop schema s_ledger_database_0043 cascade;