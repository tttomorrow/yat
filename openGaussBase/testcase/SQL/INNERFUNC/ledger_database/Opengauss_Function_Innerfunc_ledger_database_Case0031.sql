-- @testpoint: 修复指定防篡改用户表对应的全局区块表hash值，填参数汉字

--step1：建中文模式名和表名;expect:成功
drop schema if exists 模式名;
create schema 模式名 with blockchain;
drop table if exists 模式名.表名;
create table 模式名.表名(id int, name text);
select pg_catalog.ledger_gchain_repair('模式名','表名');
--step3：插入数据;expect:成功
insert into 模式名.表名 values(1, 'alex');
--step4：调用函数查看所插数据的hash值;expect:成功
select *, hash from 模式名.表名;
--step5：调用函数修复指定防篡改用户表对应的全局区块表hash值，填参数汉字;expect:返回修复过程中全局区块表hash的增量
select pg_catalog.ledger_gchain_repair('模式名','表名');
--step6：清理环境;expect:成功
drop table  模式名.表名;
drop schema 模式名 cascade;