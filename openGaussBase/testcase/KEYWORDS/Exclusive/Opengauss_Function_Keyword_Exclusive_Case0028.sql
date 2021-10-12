-- @testpoint: opengauss关键字exclusive(非保留)，作为同义词对象名，部分测试点合理报错

--前置条件
drop table if exists exclusive_test;
create table exclusive_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists exclusive;
create synonym exclusive for exclusive_test;
insert into exclusive values (1,'ada'),(2, 'bob');
update exclusive set exclusive.name='cici' where exclusive.id=2;
select * from exclusive;
drop synonym if exists exclusive;

--关键字带双引号-成功
drop synonym if exists "exclusive";
create synonym "exclusive" for exclusive_test;
drop synonym if exists "exclusive";

--关键字带单引号-合理报错
drop synonym if exists 'exclusive';
create synonym 'exclusive' for exclusive_test;
insert into 'exclusive' values (1,'ada'),(2, 'bob');
update 'exclusive' set 'exclusive'.name='cici' where 'exclusive'.id=2;
select * from 'exclusive';

--关键字带反引号-合理报错
drop synonym if exists `exclusive`;
create synonym `exclusive` for exclusive_test;
insert into `exclusive` values (1,'ada'),(2, 'bob');
update `exclusive` set `exclusive`.name='cici' where `exclusive`.id=2;
select * from `exclusive`;
drop table if exists exclusive_test;