-- @testpoint: opengauss关键字describe(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists describe_test;
create table describe_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists describe;
create synonym describe for describe_test;
insert into describe values (1,'ada'),(2, 'bob');
update describe set describe.name='cici' where describe.id=2;
select * from describe;
drop synonym describe;

--关键字带双引号-成功
drop synonym if exists "describe";
create synonym "describe" for describe_test;
drop synonym "describe";


--关键字带单引号-合理报错
drop synonym if exists 'describe';
create synonym 'describe' for describe_test;
insert into 'describe' values (1,'ada'),(2, 'bob');
update 'describe' set 'describe'.name='cici' where 'describe'.id=2;
select * from 'describe';

--关键字带反引号-合理报错
drop synonym if exists `describe`;
create synonym `describe` for describe_test;
insert into `describe` values (1,'ada'),(2, 'bob');
update `describe` set `describe`.name='cici' where `describe`.id=2;
select * from `describe`;
drop table if exists describe_test;