-- @testpoint: opengauss关键字end-exec(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists end-exec_test;
create table end-exec_test(id int,name varchar(10));

--关键字不带引号-合理报错
drop synonym if exists end-exec;
create synonym end-exec for end-exec_test;
insert into end-exec values (1,'ada'),(2, 'bob');
update end-exec set end-exec.name='cici' where end-exec.id=2;
select * from end-exec;

--关键字带双引号-合理报错
drop synonym if exists "end-exec";
create synonym "end-exec" for end-exec_test;


--关键字带单引号-合理报错
drop synonym if exists 'end-exec';
create synonym 'end-exec' for end-exec_test;
insert into 'end-exec' values (1,'ada'),(2, 'bob');
update 'end-exec' set 'end-exec'.name='cici' where 'end-exec'.id=2;
select * from 'end-exec';

--关键字带反引号-合理报错
drop synonym if exists `end-exec`;
create synonym `end-exec` for end-exec_test;
insert into `end-exec` values (1,'ada'),(2, 'bob');
update `end-exec` set `end-exec`.name='cici' where `end-exec`.id=2;
select * from `end-exec`;