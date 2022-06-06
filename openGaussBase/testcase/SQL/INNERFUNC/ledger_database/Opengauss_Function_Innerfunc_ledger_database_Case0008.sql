-- @testpoint: 校验指定防篡改用户的表级数据与hash值与其对应历史表的一致性，填参数汉字

--step1：建模式（中文模式名）建表（中文表名）;expect:成功
drop schema if exists 中文模式名;
create schema 中文模式名 with blockchain;
drop table if exists 中文模式名.中文表名;
create table 中文模式名.中文表名(id int, name text);
--step2：插入数据;expect:成功
insert into 中文模式名.中文表名 values(1, 'alex'), (2, 'bob'), (3, 'peter');
--step3：调用函数校验指定防篡改用户的表级数据与hash值与其对应历史表的一致性，填参数汉字;expect:一致返回t
select pg_catalog.ledger_hist_check('中文模式名','中文表名');
--step4：清理环境;expect:成功
drop table 中文模式名.中文表名;
drop schema 中文模式名 cascade;