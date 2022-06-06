-- @testpoint: 校验指定防篡改用户表对应的历史表hash与全局历史表对应的relhash一致，填汉字

--step1：建模式建表;expect:成功
drop schema if exists 模式;
create schema 模式 with blockchain;
drop table if exists 模式.表;
create table 模式.表(id int, name text);
--step2：插入数据;expect:成功
insert into 模式.表 values(1, 'alex'), (2, 'bob'), (3, 'peter');
--step3：调用函数校验指定防篡改用户表对应的历史表hash与全局历史表对应的relhash一致，填汉字;expect:一致则返回t
select pg_catalog.ledger_gchain_check('模式','表');
--step4：清理环境;expect:成功
drop table  模式.表;
drop schema 模式 cascade;