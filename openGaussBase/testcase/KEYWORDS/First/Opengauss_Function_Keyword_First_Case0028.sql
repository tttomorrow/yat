-- @testpoint: opengauss关键字first(非保留)，作为同义词对象名，部分测试点合理报错

--前置条件
drop table if exists first_test;
create table first_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists first;
create synonym first for first_test;
insert into first values (1,'ada'),(2, 'bob');
update first set first.name='cici' where first.id=2;
select * from first;
drop synonym if exists first;

--关键字带双引号-成功
drop synonym if exists "first";
create synonym "first" for first_test;
drop synonym if exists "first";

--关键字带单引号-合理报错
drop synonym if exists 'first';
create synonym 'first' for first_test;
insert into 'first' values (1,'ada'),(2, 'bob');
update 'first' set 'first'.name='cici' where 'first'.id=2;
select * from 'first';

--关键字带反引号-合理报错
drop synonym if exists `first`;
create synonym `first` for first_test;
insert into `first` values (1,'ada'),(2, 'bob');
update `first` set `first`.name='cici' where `first`.id=2;
select * from `first`;
drop table if exists first_test;