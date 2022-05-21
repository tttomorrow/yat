-- @testpoint: 在非篡改模式下校验指定防篡改用户的表级数据与hash值与其对应历史表的一致性，不进行增删改操作（合理报错）
--step1：建模式建表;expect:成功
drop schema if exists s_ledger_database_0041;
create schema s_ledger_database_0041;
drop table if exists s_ledger_database_0041.t_ledger_database_0041;
create table s_ledger_database_0041.t_ledger_database_0041(id int, name text);
--step2：调用函数在非篡改模式下校验指定防篡改用户的表级数据与hash值与其对应历史表的一致性;expect:失败
select pg_catalog.ledger_hist_check('s_ledger_database_0041', 't_ledger_database_0041');
--step3：清理环境;expect:成功
drop table s_ledger_database_0041.t_ledger_database_0041;
drop schema s_ledger_database_0041 cascade;