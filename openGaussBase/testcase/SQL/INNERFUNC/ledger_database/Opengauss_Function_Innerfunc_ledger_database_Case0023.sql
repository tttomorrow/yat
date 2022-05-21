-- @testpoint: 修复指定防篡改用户表对应的用户历史表hash值，用户表未损坏，填参数汉字

--step1：建中文名模式和表;expect:成功
drop schema if exists 模式名;
create schema 模式名 with blockchain;
drop table if exists 模式名.表名;
create table 模式名.表名(id int, name text);
--step2：插入数据;expect:成功
insert into 模式名.表名 values(1, 'alex'), (2, 'bob'), (3, 'peter');
--step3：调用函数修复指定防篡改用户表对应的用户历史表hash值，用户表未损坏，填参数汉字;expect:成功
select pg_catalog.ledger_hist_repair('模式名','表名');
--step4：清理环境;expect:成功
drop table  模式名.表名;
drop schema 模式名 cascade;