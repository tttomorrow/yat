-- @testpoint: 修复指定防篡改用户表对应的全局区块表hash值，全局区块表未损坏，缺一个参数schema(合理报错）

--step1：建模式建表;expect:成功
drop schema if exists s_ledger_database_0029;
create schema s_ledger_database_0029 with blockchain;
drop table if exists s_ledger_database_0029.t_ledger_database_0029;
create table s_ledger_database_0029.t_ledger_database_0029(id int, name text);
--step2：插入数据;expect:成功
insert into s_ledger_database_0029.t_ledger_database_0029 values(1, 'alex'), (2, 'bob'), (3, 'peter');
--step3：调用函数修复指定防篡改用户表对应的全局区块表hash值，全局区块表未损坏缺一个参数schema;expect:失败
select pg_catalog.ledger_gchain_repair('t_ledger_database_0029');
--step4：清理环境;expect:成功
drop table s_ledger_database_0029.t_ledger_database_0029;
drop schema s_ledger_database_0029 cascade;