-- @testpoint: opengauss关键字constraints(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists constraints_test;
create table constraints_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists constraints;
create synonym constraints for constraints_test;
insert into constraints values (1,'ada'),(2, 'bob');
update constraints set constraints.name='cici' where constraints.id=2;
select * from constraints;

--关键字带双引号-成功
drop synonym if exists "constraints";
create synonym "constraints" for constraints_test;


--关键字带单引号-合理报错
drop synonym if exists 'constraints';
create synonym 'constraints' for constraints_test;
insert into 'constraints' values (1,'ada'),(2, 'bob');
update 'constraints' set 'constraints'.name='cici' where 'constraints'.id=2;
select * from 'constraints';

--关键字带反引号-合理报错
drop synonym if exists `constraints`;
create synonym `constraints` for constraints_test;
insert into `constraints` values (1,'ada'),(2, 'bob');
update `constraints` set `constraints`.name='cici' where `constraints`.id=2;
select * from `constraints`;

--清理环境
drop synonym if exists constraints;
drop synonym if exists "constraints";
drop table if exists constraints_test;