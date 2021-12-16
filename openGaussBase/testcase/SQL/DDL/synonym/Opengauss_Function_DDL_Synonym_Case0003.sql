-- @testpoint: 为不同长度的表名创建同义词
--建表
drop table if EXISTS syn_tab_003 cascade;
create table syn_tab_003(a int,b varchar);
--建同义词
drop synonym if exists syn_a;
create synonym syn_a for syn_tab_003;
--建表，表名63位
drop table if EXISTS a23456789123456789123456789132456789123456789123456789123456789 cascade;
create table a23456789123456789123456789132456789123456789123456789123456789(a int,b varchar);
--建同义词
drop synonym if exists syn_a63;
create synonym syn_a63 for a23456789123456789123456789132456789123456789123456789123456789;
select synobjname from pg_synonym WHERE synname='syn_a63';
--建表，表名64位
drop table if EXISTS a123456789123456789123456789132456789123456789123456789123456789 cascade;
create table a123456789123456789123456789132456789123456789123456789123456789(a int,b varchar);
--建同义词
drop synonym if exists syn_a64;
create synonym syn_a64 for a123456789123456789123456789132456789123456789123456789123456789;
select synobjname from pg_synonym WHERE synname='syn_a64';
--清理环境
drop table if EXISTS syn_tab_003 cascade;
drop table if EXISTS a23456789123456789123456789132456789123456789123456789123456789 cascade;
drop table if EXISTS a123456789123456789123456789132456789123456789123456789123456789 cascade;
drop synonym if exists syn_a;
drop synonym if exists syn_a63;
drop synonym if exists syn_a64;