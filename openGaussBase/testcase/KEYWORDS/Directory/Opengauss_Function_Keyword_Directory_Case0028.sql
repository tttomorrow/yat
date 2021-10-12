-- @testpoint: opengauss关键字directory(非保留)，作为同义词对象名，部分测试点合理报错

--前置条件
drop table if exists directory_test;
create table directory_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists directory;
create synonym directory for directory_test;
insert into directory values (1,'ada'),(2, 'bob');
update directory set directory.name='cici' where directory.id=2;
select * from directory;
drop synonym if exists directory;

--关键字带双引号-成功
drop synonym if exists "directory";
create synonym "directory" for directory_test;
drop synonym if exists "directory";

--关键字带单引号-合理报错
drop synonym if exists 'directory';
create synonym 'directory' for directory_test;
insert into 'directory' values (1,'ada'),(2, 'bob');
update 'directory' set 'directory'.name='cici' where 'directory'.id=2;
select * from 'directory';

--关键字带反引号-合理报错
drop synonym if exists `directory`;
create synonym `directory` for directory_test;
insert into `directory` values (1,'ada'),(2, 'bob');
update `directory` set `directory`.name='cici' where `directory`.id=2;
select * from `directory`;
drop table if exists directory_test;