-- @testpoint: 创建同义词为无效标识符，合理报错
-- @modify at: 2020-11-25
--建表
drop table if EXISTS test_synonym cascade;
create table test_synonym(a int,b varchar);
--单个字符
drop synonym if EXISTS 0 cascade;
drop synonym if EXISTS $ cascade;
drop synonym if EXISTS ! cascade;
drop synonym if EXISTS # cascade;
drop synonym if EXISTS @ cascade;
drop synonym if EXISTS ^ cascade;
drop synonym if EXISTS & cascade;
drop synonym if EXISTS * cascade;
drop synonym if EXISTS ( cascade;
drop synonym if EXISTS ) cascade;
drop synonym if EXISTS - cascade;
drop synonym if EXISTS = cascade;
drop synonym if EXISTS + cascade;
drop synonym if EXISTS ` cascade;
drop synonym if EXISTS ~ cascade;
drop synonym if EXISTS . cascade;
create synonym 0 for test_synonym;
create synonym $ for test_synonym;
create synonym ! for test_synonym;
create synonym # for test_synonym;
create synonym @ for test_synonym;
create synonym ^ for test_synonym;
create synonym & for test_synonym;
create synonym * for test_synonym;
create synonym ( for test_synonym;
create synonym ) for test_synonym;
create synonym - for test_synonym;
create synonym = for test_synonym;
create synonym + for test_synonym;
create synonym ` for test_synonym;
create synonym ~ for test_synonym;
create synonym . for test_synonym;
--组合场景
drop synonym if EXISTS 0aA cascade;
drop synonym if EXISTS $aA cascade;
drop synonym if EXISTS $a cascade;
drop synonym if EXISTS 0__ cascade;
drop synonym if EXISTS 0_$ cascade;
drop synonym if EXISTS 0_$aA cascade;
drop synonym if EXISTS $__ cascade;
drop synonym if EXISTS $_0 cascade;
drop synonym if EXISTS $_0aA cascade;
create synonym 0aA for test_synonym;
create synonym $aA for test_synonym;
create synonym $a for test_synonym;
create synonym 0__ for test_synonym;
create synonym 0_$ for test_synonym;
create synonym 0_$aA for test_synonym;
create synonym $__ for test_synonym;
create synonym $_0 for test_synonym;
create synonym $_0aA for test_synonym;
--清理环境
drop synonym if EXISTS 0aA cascade;
drop synonym if EXISTS $aA cascade;
drop synonym if EXISTS $a cascade;
drop synonym if EXISTS 0__ cascade;
drop synonym if EXISTS 0_$ cascade;
drop synonym if EXISTS 0_$aA cascade;
drop synonym if EXISTS $__ cascade;
drop synonym if EXISTS $_0 cascade;
drop synonym if EXISTS $_0aA cascade;
