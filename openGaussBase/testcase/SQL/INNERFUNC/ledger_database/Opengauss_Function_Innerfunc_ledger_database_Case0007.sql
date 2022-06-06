-- @testpoint: 校验指定防篡改用户的表级数据与hash值与其对应历史表的一致性，不填参数（合理报错）

--step1：建模式建表;expect:成功
drop schema if exists s_ledger_database_007;
create schema s_ledger_database_007 with blockchain;
drop table if exists s_ledger_database_007.t_ledger_database_007;
create table s_ledger_database_007.t_ledger_database_007(id int, name text);
--step2：插入数据;expect:成功
insert into  s_ledger_database_007.t_ledger_database_007 values(1, 'alex'), (2, 'bob'), (3, 'peter');
--step3：调用函数校验指定防篡改用户的表级数据与hash值与其对应历史表的一致性，不填参数;expect:失败
select pg_catalog.ledger_hist_check();
--step4：清理环境;expect:成功
drop table  s_ledger_database_007.t_ledger_database_007;
drop schema s_ledger_database_007 cascade;