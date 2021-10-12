-- @testpoint: opengauss关键字execute(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists execute_test;
create table execute_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists execute;
create synonym execute for execute_test;
insert into execute values (1,'ada'),(2, 'bob');
update execute set execute.name='cici' where execute.id=2;
select * from execute;
drop synonym if exists execute;

--关键字带双引号-成功
drop synonym if exists "execute";
create synonym "execute" for execute_test;
drop synonym if exists "execute";

--关键字带单引号-合理报错
drop synonym if exists 'execute';
create synonym 'execute' for execute_test;
insert into 'execute' values (1,'ada'),(2, 'bob');
update 'execute' set 'execute'.name='cici' where 'execute'.id=2;
select * from 'execute';

--关键字带反引号-合理报错
drop synonym if exists `execute`;
create synonym `execute` for execute_test;
insert into `execute` values (1,'ada'),(2, 'bob');
update `execute` set `execute`.name='cici' where `execute`.id=2;
select * from `execute`;
drop table if exists execute_test;