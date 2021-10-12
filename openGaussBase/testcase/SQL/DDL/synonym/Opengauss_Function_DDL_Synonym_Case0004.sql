-- @testpoint: 创建同义词为有效标识符，创建成功
-- @modify at: 2020-11-25
--建表
drop table if EXISTS test_synonym cascade;
create table test_synonym(a int,b varchar);
--同义词名为单个字母
drop synonym if EXISTS a cascade;
create synonym a for test_synonym;
drop synonym if EXISTS "A" cascade;
create synonym "A" for test_synonym;
--同义词名为下划线
drop synonym if EXISTS _ cascade;
create synonym _ for test_synonym;
--查询同义词信息
select synobjname from pg_synonym WHERE synname='a';
select synobjname from pg_synonym WHERE synname='_';
select synobjname from pg_synonym WHERE synname='A';
--单类型
drop synonym if EXISTS abz cascade;
drop synonym if EXISTS "ABZ" cascade;
drop synonym if EXISTS ___ cascade;
create synonym abz for test_synonym;
create synonym "ABZ" for test_synonym;
create synonym ___ for test_synonym;
--查询同义词信息
select synobjname from pg_synonym WHERE synname='abz';
select synobjname from pg_synonym WHERE synname='ABZ';
select synobjname from pg_synonym WHERE synname='___';
--组合类型
drop synonym if EXISTS "aA" cascade;
drop synonym if EXISTS "Bz" cascade;
drop synonym if EXISTS "_aA" cascade;
drop synonym if EXISTS _$ cascade;
drop synonym if EXISTS _0 cascade;
drop synonym if EXISTS "aA$" cascade;
drop synonym if EXISTS _$0 cascade;
drop synonym if EXISTS "_$Aa" cascade;
drop synonym if EXISTS _0$ cascade;
drop synonym if EXISTS "_A$0" cascade;
create synonym "aA" for test_synonym;
create synonym "Bz" for test_synonym;
create synonym "_aA" for test_synonym;
create synonym _$ for test_synonym;
create synonym _0 for test_synonym;
create synonym "aA$" for test_synonym;
create synonym _$0 for test_synonym;
create synonym "_$Aa" for test_synonym;
create synonym _0$ for test_synonym;
create synonym "_A$0" for test_synonym;
--查询同义词信息
select synobjname from pg_synonym WHERE synname='aA';
select synobjname from pg_synonym WHERE synname='Bz';
select synobjname from pg_synonym WHERE synname='_aA';
select synobjname from pg_synonym WHERE synname='_0';
select synobjname from pg_synonym WHERE synname='aA$';
select synobjname from pg_synonym WHERE synname='_$0';
select synobjname from pg_synonym WHERE synname='_$Aa';
select synobjname from pg_synonym WHERE synname='_0$';
select synobjname from pg_synonym WHERE synname='_A$0';
--清理数据
drop table if EXISTS test_synonym cascade;
drop synonym if EXISTS a cascade;
drop synonym if EXISTS "A" cascade;
drop synonym if EXISTS _ cascade;
drop synonym if EXISTS abz cascade;
drop synonym if EXISTS "ABZ" cascade;
drop synonym if EXISTS ___ cascade;
drop synonym if EXISTS "aA" cascade;
drop synonym if EXISTS "Bz" cascade;
drop synonym if EXISTS "_aA" cascade;
drop synonym if EXISTS _$ cascade;
drop synonym if EXISTS _0 cascade;
drop synonym if EXISTS "aA$" cascade;
drop synonym if EXISTS _$0 cascade;
drop synonym if EXISTS "_$Aa" cascade;
drop synonym if EXISTS _0$ cascade;
drop synonym if EXISTS "_A$0" cascade;