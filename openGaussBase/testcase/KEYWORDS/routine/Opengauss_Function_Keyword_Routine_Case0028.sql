-- @testpoint: opengauss关键字routine(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists routine_test;
create table routine_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists routine;
create synonym routine for routine_test;
insert into routine values (1,'ada'),(2, 'bob');
update routine set routine.name='cici' where routine.id=2;
select * from routine;

--清理环境
drop synonym if exists routine;

--关键字带双引号-成功
drop synonym if exists "routine";
create synonym "routine" for routine_test;
insert into "routine" values (1,'ada'),(2, 'bob');
update "routine" set "routine".name='cici' where "routine".id=2;
select * from "routine";

--清理环境
drop synonym if exists "routine";

--关键字带单引号-合理报错
drop synonym if exists 'routine';

--关键字带反引号-合理报错
drop synonym if exists `routine`;
drop table if exists routine_test;