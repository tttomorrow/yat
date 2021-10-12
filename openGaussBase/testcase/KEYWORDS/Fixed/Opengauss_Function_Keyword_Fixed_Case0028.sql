-- @testpoint: opengauss关键字fixed(非保留)，作为同义词对象名，部分测试点合理报错

--前置条件
drop table if exists fixed_test;
create table fixed_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists fixed;
create synonym fixed for fixed_test;
insert into fixed values (1,'ada'),(2, 'bob');
update fixed set fixed.name='cici' where fixed.id=2;
select * from fixed;
drop synonym if exists fixed;

--关键字带双引号-成功
drop synonym if exists "fixed";
create synonym "fixed" for fixed_test;
drop synonym if exists "fixed";

--关键字带单引号-合理报错
drop synonym if exists 'fixed';
create synonym 'fixed' for fixed_test;
insert into 'fixed' values (1,'ada'),(2, 'bob');
update 'fixed' set 'fixed'.name='cici' where 'fixed'.id=2;
select * from 'fixed';

--关键字带反引号-合理报错
drop synonym if exists `fixed`;
create synonym `fixed` for fixed_test;
insert into `fixed` values (1,'ada'),(2, 'bob');
update `fixed` set `fixed`.name='cici' where `fixed`.id=2;
select * from `fixed`;
drop table if exists fixed_test;