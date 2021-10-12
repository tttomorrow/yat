-- @testpoint: opengauss关键字defined(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists defined_test;
create table defined_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists defined;
create synonym defined for defined_test;
insert into defined values (1,'ada'),(2, 'bob');
update defined set defined.name='cici' where defined.id=2;
select * from defined;
drop synonym if exists defined;

--关键字带双引号-成功
drop synonym if exists "defined";
create synonym "defined" for defined_test;
drop synonym if exists "defined";

--关键字带单引号-合理报错
drop synonym if exists 'defined';
create synonym 'defined' for defined_test;
insert into 'defined' values (1,'ada'),(2, 'bob');
update 'defined' set 'defined'.name='cici' where 'defined'.id=2;
select * from 'defined';

--关键字带反引号-合理报错
drop synonym if exists `defined`;
create synonym `defined` for defined_test;
insert into `defined` values (1,'ada'),(2, 'bob');
update `defined` set `defined`.name='cici' where `defined`.id=2;
select * from `defined`;
drop table if exists defined_test;