-- @testpoint: opengauss关键字exec(非保留)，作为同义词对象名，部分测试点合理报错

--前置条件
drop table if exists exec_test;
create table exec_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists exec;
create synonym exec for exec_test;
insert into exec values (1,'ada'),(2, 'bob');
update exec set exec.name='cici' where exec.id=2;
select * from exec;
drop synonym if exists exec;

--关键字带双引号-成功
drop synonym if exists "exec";
create synonym "exec" for exec_test;
drop synonym if exists "exec";

--关键字带单引号-合理报错
drop synonym if exists 'exec';
create synonym 'exec' for exec_test;
insert into 'exec' values (1,'ada'),(2, 'bob');
update 'exec' set 'exec'.name='cici' where 'exec'.id=2;
select * from 'exec';

--关键字带反引号-合理报错
drop synonym if exists `exec`;
create synonym `exec` for exec_test;
insert into `exec` values (1,'ada'),(2, 'bob');
update `exec` set `exec`.name='cici' where `exec`.id=2;
select * from `exec`;
drop table if exists exec_test;