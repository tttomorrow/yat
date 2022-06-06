-- @testpoint: 修复指定防篡改用户表对应的全局区块表hash值，区块表未损坏，不填参数（合理报错）

--step1：建模式建表;expect:成功
drop schema if exists s_ledger_database_0030;
create schema s_ledger_database_0030 with blockchain;
drop table if exists s_ledger_database_0030.t_ledger_database_0030;
create table s_ledger_database_0030.t_ledger_database_0030(id int, name text);
--step2：插入数据;expect:成功
insert into s_ledger_database_0030.t_ledger_database_0030 values(1, 'alex'), (2, 'bob'), (3, 'peter');
--step3：调用函数修复指定防篡改用户表对应的全局区块表hash值，区块表未损坏，不填参数;expect:失败
select pg_catalog.ledger_gchain_repair();
--step4：清理环境;expect:成功
drop table  s_ledger_database_0030.t_ledger_database_0030;
drop schema s_ledger_database_0030 cascade;