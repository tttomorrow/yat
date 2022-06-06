-- @testpoint: 校验指定防篡改用户的表级数据与hash值与其对应历史表的一致性，进行增改操作

--step1：建模式建表;expect:成功
drop schema if exists s_ledger_database_002;
create schema s_ledger_database_002 with blockchain;
drop table if exists s_ledger_database_002.t_ledger_database_002;
create table s_ledger_database_002.t_ledger_database_002(id int, name text);
--step2：插入修改数据;expect:成功
insert into  s_ledger_database_002.t_ledger_database_002 values(1, 'alex'), (2, 'bob'), (3, 'peter');
update  s_ledger_database_002.t_ledger_database_002 set name = 'bob2' where id = 2;
--step3：调用函数校验进行增改操作后的表级数据与hash值与其对应历史表的一致性;expect:成功
select pg_catalog.ledger_hist_check('s_ledger_database_002', 't_ledger_database_002');
--step4：清理环境;expect:成功
drop table  s_ledger_database_002.t_ledger_database_002;
drop schema s_ledger_database_002 cascade;