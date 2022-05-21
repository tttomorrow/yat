-- @testpoint: 创建同义词，同义词名称测试
-- @modify at: 2020-11-25
--建表
drop table if exists syn_tab_002 cascade;
create table syn_tab_002(a int,b varchar);
--创建同义词
drop synonym if exists syn_tab_002_bak ;
create synonym syn_tab_002_bak for syn_tab_002;
--63位标识符，有效
create synonym a23456789123456789123456789132456789123456789123456789123456789 for syn_tab_002;
select synname from pg_synonym where synname like 'a23456789123456789123456789132456789%';
--64为标识符，被截取为63位后存储引用
create synonym a123456789123456789123456789132456789123456789123456789123456789 for syn_tab_002;
select synname from pg_synonym where synname like 'a123456789123456789123456789132456789%';
--清理数据
drop table if exists syn_tab_002 cascade;
drop synonym if exists syn_tab_002_bak;
drop synonym if exists a23456789123456789123456789132456789123456789123456789123456789;
drop synonym if exists a12345678912345678912345678913245678912345678912345678912345678;
