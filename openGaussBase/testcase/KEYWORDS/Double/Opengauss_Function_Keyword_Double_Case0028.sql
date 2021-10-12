-- @testpoint: opengauss关键字double(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists double_test;
create table double_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists double;
create synonym double for double_test;
insert into double values (1,'ada'),(2, 'bob');
update double set double.name='cici' where double.id=2;
select * from double;
drop synonym if exists double;

--关键字带双引号-成功
drop synonym if exists "double";
create synonym "double" for double_test;
drop synonym if exists "double";

--关键字带单引号-合理报错
drop synonym if exists 'double';
create synonym 'double' for double_test;
insert into 'double' values (1,'ada'),(2, 'bob');
update 'double' set 'double'.name='cici' where 'double'.id=2;
select * from 'double';

--关键字带反引号-合理报错
drop synonym if exists `double`;
create synonym `double` for double_test;
insert into `double` values (1,'ada'),(2, 'bob');
update `double` set `double`.name='cici' where `double`.id=2;
select * from `double`;
drop table if exists double_test;