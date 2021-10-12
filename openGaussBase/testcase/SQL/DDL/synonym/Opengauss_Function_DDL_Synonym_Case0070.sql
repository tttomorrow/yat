-- @testpoint: 创建临时表的同义词，修改同义词属主（属主为存在+不存在+存在无create权限）,不存在+存在无create权限,合理报错
-- @modify at: 2020-11-26
--建表
CREATE TEMPORARY table test_tempsyn(id int);
insert into test_tempsyn values(1);
select * from test_tempsyn;
--创建同义词
drop synonym if exists tmp_syn_01;
create synonym tmp_syn_01 for test_tempsyn;
select * from tmp_syn_01;
--创建用户
drop user if exists syn007 cascade;
create user syn007 password "Test@123";
--修改为存在的属主：新属主无create权限：报错
alter synonym tmp_syn_01 owner to syn007;
--修改为不存在的属主：报错
drop user if exists test_syn05 cascade;
alter synonym tmp_syn_01 owner to test_syn05;
--修改为存在的属主：新属主有create权限
GRANT ALL PRIVILEGES TO syn007;
alter synonym tmp_syn_01 owner to syn007;
--清理环境
drop user if exists syn007 cascade;
drop table if exists test_synonym cascade;
drop synonym if exists tmp_syn_01;