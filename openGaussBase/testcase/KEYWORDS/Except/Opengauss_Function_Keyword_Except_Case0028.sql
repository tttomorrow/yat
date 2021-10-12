-- @testpoint: opengauss关键字except(保留)，作为同义词对象名，部分测试点合理报错

--前置条件
drop table if exists except_test;
create table except_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists except;
create synonym except for except_test;


--关键字带双引号-成功
drop synonym if exists "except";
create synonym "except" for except_test;
insert into "except" values (1,'ada'),(2, 'bob');
update "except" set "except".name='cici' where "except".id=2;
select * from "except";
drop synonym "except";
--关键字带单引号-合理报错
drop synonym if exists 'except';
create synonym 'except' for except_test;
insert into 'except' values (1,'ada'),(2, 'bob');
update 'except' set 'except'.name='cici' where 'except'.id=2;
select * from 'except';

--关键字带反引号-合理报错
drop synonym if exists `except`;
create synonym `except` for except_test;
insert into `except` values (1,'ada'),(2, 'bob');
update `except` set `except`.name='cici' where `except`.id=2;
select * from `except`;
drop table if exists except_test;