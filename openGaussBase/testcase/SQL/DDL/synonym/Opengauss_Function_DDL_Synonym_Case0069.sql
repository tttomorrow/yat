-- @testpoint: 创建视图的同义词，修改同义词属主（属主为存在+不存在+存在无create权限）,不存在+存在无create权限,合理报错

--建表
drop table if EXISTS test_synonym cascade;
create table test_synonym(a int,b varchar);
insert into test_synonym values(1,'a');
--建视图
drop view if exists test_synview;
create view test_synview as select * from test_synonym;
--创建视图同义词
drop synonym if EXISTS synview cascade;
create synonym synview for test_synview;
--创建用户
drop user if exists syn006;
create user syn006 password "Mima@123";
--修改为存在的属主：新属主无create权限：报错
alter synonym synview owner to syn006;
--修改为不存在的属主：报错
drop user if exists test_syn05;
alter synonym synview owner to test_syn05;
--修改为存在的属主：新属主有create权限
GRANT ALL PRIVILEGES TO syn006;
alter synonym synview owner to syn006;
--清理数据
drop user if exists syn006 cascade;
drop synonym if exists synview cascade;
drop table if exists test_synonym cascade;