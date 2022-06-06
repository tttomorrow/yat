-- @testpoint: 校验指定防篡改用户表对应的历史表hash与全局历史表对应的relhash一致性，缺一个参数表名（合理报错）

--step1：建模式建表;expect:成功
drop schema if exists s_ledger_database_0015;
create schema s_ledger_database_0015 with blockchain;
drop table if exists s_ledger_database_0015.t_ledger_database_0015;
create table s_ledger_database_0015.t_ledger_database_0015(id int, name text);
--step2：插入数据;expect:成功
insert into s_ledger_database_0015.t_ledger_database_0015 values(1, 'alex'), (2, 'bob'), (3, 'peter');
--step3：校验指定防篡改用户表对应的历史表hash与全局历史表对应的relhash一致性，缺一个参数表名;expect:失败
select pg_catalog.ledger_gchain_check('s_ledger_database_0015');
--step4：清理环境;expect:成功
drop table  s_ledger_database_0015.t_ledger_database_0015;
drop schema s_ledger_database_0015 cascade;