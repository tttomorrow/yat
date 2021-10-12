-- @testpoint: 插入超出范围值，合理报错
-- @modify at: 2020-11-17

drop table if exists test_varchar2_10;
create table test_varchar2_10 (name varchar2(20));
insert into test_varchar2_10 values ('QWERTSGYUOEOCMLW;PEIOPEUIEYUDGSS');
insert into test_varchar2_10 values ('高斯开源数据库');
drop table test_varchar2_10;