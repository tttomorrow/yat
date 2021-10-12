-- @testpoint: opengauss关键字discard(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists discard_test;
create table discard_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists discard;
create synonym discard for discard_test;
insert into discard values (1,'ada'),(2, 'bob');
update discard set discard.name='cici' where discard.id=2;
select * from discard;
drop synonym if exists discard;

--关键字带双引号-成功
drop synonym if exists "discard";
create synonym "discard" for discard_test;
drop synonym if exists "discard";

--关键字带单引号-合理报错
drop synonym if exists 'discard';
create synonym 'discard' for discard_test;
insert into 'discard' values (1,'ada'),(2, 'bob');
update 'discard' set 'discard'.name='cici' where 'discard'.id=2;
select * from 'discard';

--关键字带反引号-合理报错
drop synonym if exists `discard`;
create synonym `discard` for discard_test;
insert into `discard` values (1,'ada'),(2, 'bob');
update `discard` set `discard`.name='cici' where `discard`.id=2;
select * from `discard`;
drop table if exists discard_test;