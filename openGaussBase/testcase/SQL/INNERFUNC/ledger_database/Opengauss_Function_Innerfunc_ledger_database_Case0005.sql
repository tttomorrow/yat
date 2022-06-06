-- @testpoint: 校验指定防篡改用户的表级数据与hash值与其对应历史表的一致性，缺一个参数schema（合理报错）

--step1：建模式建表;expect:成功
drop schema if exists s_ledger_database_005;
create schema s_ledger_database_005 with blockchain;
drop table if exists s_ledger_database_005.t_ledger_database_005;
create table s_ledger_database_005.t_ledger_database_005(id int, name text);
--step2：插入数据;expect:成功
insert into s_ledger_database_005.t_ledger_database_005 values(1, 'alex'), (2, 'bob'), (3, 'peter');
--step3：调用函数校验指定防篡改用户的表级数据与hash值与其对应历史表的一致性，缺一个参数schema;expect:失败
select pg_catalog.ledger_hist_check('t_ledger_database_005');
--step4：清理环境;expect:成功
drop table  s_ledger_database_005.t_ledger_database_005;
drop schema s_ledger_database_005 cascade;