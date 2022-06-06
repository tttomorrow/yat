-- @testpoint: 修复指定防篡改用户表对应的全局区块表hash值，进行增删改操作


--step1：建模式建表;expect:成功
drop schema if exists s_ledger_database_0027;
create schema s_ledger_database_0027 with blockchain;
drop table if exists s_ledger_database_0027.t_ledger_database_0027;
create table s_ledger_database_0027.t_ledger_database_0027(id int, name text);
--step2：插入修改删除数据;expect:成功
insert into s_ledger_database_0027.t_ledger_database_0027 values(1, 'alex'), (2, 'bob'), (3, 'peter');
update  s_ledger_database_0027.t_ledger_database_0027 set name = 'bob2' where id = 2;
delete from s_ledger_database_0027.t_ledger_database_0027 where  id = 3;
--step3：调用函数修复指定防篡改用户表对应的全局区块表hash值，进行增删改操作;expect:返回修复过程中的hash值增量
select pg_catalog.ledger_gchain_repair('s_ledger_database_0027', 't_ledger_database_0027');
--step4：清理环境;expect:成功
drop table  s_ledger_database_0027.t_ledger_database_0027;
drop schema s_ledger_database_0027 cascade;