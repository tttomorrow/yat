-- @testpoint: opengauss关键字declare(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists declare_test;
create table declare_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists declare;
create synonym declare for declare_test;
insert into declare values (1,'ada'),(2, 'bob');
update declare set declare.name='cici' where declare.id=2;
select * from declare;
drop synonym if exists declare;

--关键字带双引号-成功
drop synonym if exists "declare";
create synonym "declare" for declare_test;
drop synonym if exists "declare";

--关键字带单引号-合理报错
drop synonym if exists 'declare';
create synonym 'declare' for declare_test;
insert into 'declare' values (1,'ada'),(2, 'bob');
update 'declare' set 'declare'.name='cici' where 'declare'.id=2;
select * from 'declare';

--关键字带反引号-合理报错
drop synonym if exists `declare`;
create synonym `declare` for declare_test;
insert into `declare` values (1,'ada'),(2, 'bob');
update `declare` set `declare`.name='cici' where `declare`.id=2;
select * from `declare`;
drop table if exists declare_test;