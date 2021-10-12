-- @testpoint: opengauss关键字concurrently(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists concurrently_test;
create table concurrently_test(id int,name varchar(10));

--关键字不带引号-合理报错
drop synonym if exists concurrently;
create synonym concurrently for concurrently_test;
insert into concurrently values (1,'ada'),(2, 'bob');
update concurrently set concurrently.name='cici' where concurrently.id=2;
select * from concurrently;

--关键字带双引号-成功
drop synonym if exists "concurrently";
create synonym "concurrently" for concurrently_test;
drop synonym if exists "concurrently";

--关键字带单引号-合理报错
drop synonym if exists 'concurrently';
create synonym 'concurrently' for concurrently_test;
insert into 'concurrently' values (1,'ada'),(2, 'bob');
update 'concurrently' set 'concurrently'.name='cici' where 'concurrently'.id=2;
select * from 'concurrently';

--关键字带反引号-合理报错
drop synonym if exists `concurrently`;
create synonym `concurrently` for concurrently_test;
insert into `concurrently` values (1,'ada'),(2, 'bob');
update `concurrently` set `concurrently`.name='cici' where `concurrently`.id=2;
select * from `concurrently`;
drop table if exists concurrently_test;