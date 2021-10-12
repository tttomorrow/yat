-- @testpoint: opengauss关键字restart(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists restart_test;
create table restart_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists restart;
create synonym restart for restart_test;
insert into restart values (1,'ada'),(2, 'bob');
update restart set restart.name='cici' where restart.id=2;
select * from restart;
drop synonym if exists restart;

--关键字带双引号-成功
drop synonym if exists "restart";
create synonym "restart" for restart_test;
insert into "restart" values (1,'ada'),(2, 'bob');
update "restart" set "restart".name='cici' where "restart".id=2;
select * from "restart";
drop synonym if exists "restart";

--关键字带单引号-合理报错
drop synonym if exists 'restart';

--关键字带反引号-合理报错
drop synonym if exists `restart`;
drop table if exists restart_test;