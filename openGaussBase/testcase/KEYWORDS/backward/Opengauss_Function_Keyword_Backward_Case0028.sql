-- @testpoint: opengauss关键字backward(非保留)，作为同义词对象名,部分测试点合理报错
--前置条件
drop table if exists backward_test;
create table backward_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists backward;
create synonym backward for backward_test;
insert into backward values (1,'ada'),(2, 'bob');
update backward set backward.name='cici' where backward.id=2;
select * from backward;

--清理环境
drop synonym if exists backward;

--关键字带双引号-成功
drop synonym if exists "backward";
create synonym "backward" for backward_test;
insert into "backward" values (1,'ada'),(2, 'bob');
update "backward" set "backward".name='cici' where "backward".id=2;
select * from "backward";

--清理环境
drop synonym if exists "backward";

--关键字带单引号-合理报错
drop synonym if exists 'backward';

--关键字带反引号-合理报错
drop synonym if exists `backward`;
drop table if exists backward_test;