-- @testpoint: 创建表的同义词，修改同义词属主（属主为存在+不存在+存在无create权限）,不存在+存在无create权限,合理报错
-- @modify at: 2020-11-26
--建表
drop table if EXISTS test_synonym cascade;
create table test_synonym(a int,b varchar);
insert into test_synonym values(1,'a');
--创建同义词
drop synonym if EXISTS test_alter cascade;
create synonym test_alter for test_synonym;
--创建用户
drop user if exists syn003 cascade;
create user syn003 password 'Test@123';
--修改同义词为存在的属主：新属主无create权限，合理报错
alter synonym test_alter owner to syn003;
--修改为不存在的属主：报错
drop user if exists test_syn05;
alter synonym test_alter owner to test_syn05;
--修改为存在的属主：新属主有create权限
GRANT ALL PRIVILEGES TO syn003;
alter synonym test_alter owner to syn003;
--清理数据
drop user if exists syn003 cascade;
drop table if EXISTS test_synonym cascade;
drop synonym if EXISTS test_alter cascade;