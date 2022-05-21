-- @testpoint: 在非篡改模式下修复指定防篡改用户表对应的全局区块表hash值，进行增删改操作（合理报错）


--step1：建模式建表;expect:成功
drop schema if exists s_ledger_database_0037;
create schema s_ledger_database_0037;
drop table if exists s_ledger_database_0037.t_ledger_database_0037;
create table s_ledger_database_0037.t_ledger_database_0037(id int, name text);
--step2：插入修改删除数据;expect:成功
insert into s_ledger_database_0037.t_ledger_database_0037 values(1, 'alex'), (2, 'bob'), (3, 'peter');
update  s_ledger_database_0037.t_ledger_database_0037 set name = 'bob2' where id = 2;
delete from s_ledger_database_0037.t_ledger_database_0037 where  id = 3;
--step3：调用函数在非篡改模式下修复指定防篡改用户表对应的全局区块表hash值，进行增删改操作;expect:失败
select pg_catalog.ledger_gchain_repair('s_ledger_database_0037', 't_ledger_database_0037');
--step4：清理环境;expect:成功
drop table  s_ledger_database_0037.t_ledger_database_0037;
drop schema s_ledger_database_0037 cascade;