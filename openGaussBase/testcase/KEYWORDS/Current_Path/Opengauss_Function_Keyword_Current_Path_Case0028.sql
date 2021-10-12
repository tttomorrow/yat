-- @testpoint: opengauss关键字current_path(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists current_path_test;
create table current_path_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists current_path;
create synonym current_path for current_path_test;
insert into current_path values (1,'ada'),(2, 'bob');
update current_path set current_path.name='cici' where current_path.id=2;
select * from current_path;
drop synonym if exists current_path;

--关键字带双引号-成功
drop synonym if exists "current_path";
create synonym "current_path" for current_path_test;
drop synonym if exists "current_path";

--关键字带单引号-合理报错
drop synonym if exists 'current_path';
create synonym 'current_path' for current_path_test;
insert into 'current_path' values (1,'ada'),(2, 'bob');
update 'current_path' set 'current_path'.name='cici' where 'current_path'.id=2;
select * from 'current_path';

--关键字带反引号-合理报错
drop synonym if exists `current_path`;
create synonym `current_path` for current_path_test;
insert into `current_path` values (1,'ada'),(2, 'bob');
update `current_path` set `current_path`.name='cici' where `current_path`.id=2;
select * from `current_path`;
drop table if exists current_path_test;