-- @testpoint: opengauss关键字dbcompatibility(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists dbcompatibility_test;
create table dbcompatibility_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists dbcompatibility;
create synonym dbcompatibility for dbcompatibility_test;
insert into dbcompatibility values (1,'ada'),(2, 'bob');
update dbcompatibility set dbcompatibility.name='cici' where dbcompatibility.id=2;
select * from dbcompatibility;
drop synonym if exists dbcompatibility;

--关键字带双引号-成功
drop synonym if exists "dbcompatibility";
create synonym "dbcompatibility" for dbcompatibility_test;
drop synonym if exists "dbcompatibility";

--关键字带单引号-合理报错
drop synonym if exists 'dbcompatibility';
create synonym 'dbcompatibility' for dbcompatibility_test;
insert into 'dbcompatibility' values (1,'ada'),(2, 'bob');
update 'dbcompatibility' set 'dbcompatibility'.name='cici' where 'dbcompatibility'.id=2;
select * from 'dbcompatibility';

--关键字带反引号-合理报错
drop synonym if exists `dbcompatibility`;
create synonym `dbcompatibility` for dbcompatibility_test;
insert into `dbcompatibility` values (1,'ada'),(2, 'bob');
update `dbcompatibility` set `dbcompatibility`.name='cici' where `dbcompatibility`.id=2;
select * from `dbcompatibility`;
drop table if exists dbcompatibility_test;