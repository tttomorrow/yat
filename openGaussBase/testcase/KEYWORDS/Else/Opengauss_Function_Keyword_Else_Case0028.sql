-- @testpoint: opengauss关键字else(保留)，作为同义词对象名，部分测试点合理报错

--前置条件
drop table if exists else_test;
create table else_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists else;
create synonym else for else_test;


--关键字带双引号-成功
drop synonym if exists "else";
create synonym "else" for else_test;
insert into "else" values (1,'ada'),(2, 'bob');
update "else" set "else".name='cici' where "else".id=2;
select * from "else";
drop synonym "else";
--关键字带单引号-合理报错
drop synonym if exists 'else';
create synonym 'else' for else_test;
insert into 'else' values (1,'ada'),(2, 'bob');
update 'else' set 'else'.name='cici' where 'else'.id=2;
select * from 'else';

--关键字带反引号-合理报错
drop synonym if exists `else`;
create synonym `else` for else_test;
insert into `else` values (1,'ada'),(2, 'bob');
update `else` set `else`.name='cici' where `else`.id=2;
select * from `else`;
drop table if exists else_test;