-- @testpoint: opengauss关键字routine_name(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists routine_name;
create synonym routine_name for explain_test;
insert into routine_name values (1,'ada'),(2, 'bob');
update routine_name set routine_name.name='cici' where routine_name.id=2;
select * from routine_name;
drop synonym if exists routine_name;

--关键字带双引号-成功
drop synonym if exists "routine_name";
create synonym "routine_name" for explain_test;
drop synonym if exists "routine_name";

--关键字带单引号-合理报错
drop synonym if exists 'routine_name';
create synonym 'routine_name' for explain_test;
insert into 'routine_name' values (1,'ada'),(2, 'bob');
update 'routine_name' set 'routine_name'.name='cici' where 'routine_name'.id=2;
select * from 'routine_name';

--关键字带反引号-合理报错
drop synonym if exists `routine_name`;
create synonym `routine_name` for explain_test;
insert into `routine_name` values (1,'ada'),(2, 'bob');
update `routine_name` set `routine_name`.name='cici' where `routine_name`.id=2;
select * from `routine_name`;
drop table if exists explain_test;