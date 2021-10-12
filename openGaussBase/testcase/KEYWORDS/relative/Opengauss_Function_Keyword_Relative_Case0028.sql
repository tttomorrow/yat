-- @testpoint: opengauss关键字relative(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists relative_test;
create table relative_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists relative;
create synonym relative for relative_test;
insert into relative values (1,'ada'),(2, 'bob');
update relative set relative.name='cici' where relative.id=2;
select * from relative;
drop synonym if exists relative;

--关键字带双引号-成功
drop synonym if exists "relative";
create synonym "relative" for relative_test;
insert into "relative" values (1,'ada'),(2, 'bob');
update "relative" set "relative".name='cici' where "relative".id=2;
select * from "relative";
drop synonym if exists "relative";

--关键字带单引号-合理报错
drop synonym if exists 'relative';

--关键字带反引号-合理报错
drop synonym if exists `relative`;
drop table if exists relative_test;