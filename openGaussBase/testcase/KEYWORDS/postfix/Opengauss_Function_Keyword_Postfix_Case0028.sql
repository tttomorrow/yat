-- @testpoint: opengauss关键字postfix(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists postfix_test;
create table postfix_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists postfix;
create synonym postfix for postfix_test;
insert into postfix values (1,'ada'),(2, 'bob');
update postfix set postfix.name='cici' where postfix.id=2;
select * from postfix;

--关键字带双引号-成功
drop synonym if exists "postfix";
create synonym "postfix" for postfix_test;
insert into "postfix" values (1,'ada'),(2, 'bob');
update "postfix" set "postfix".name='cici' where "postfix".id=2;
select * from "postfix";

--关键字带单引号-合理报错
drop synonym if exists 'postfix';
create synonym 'postfix' for postfix_test;

--关键字带反引号-合理报错
drop synonym if exists `postfix`;
create synonym `postfix` for postfix_test;
--清理环境
drop synonym if exists "postfix";
drop synonym if exists postfix;
drop table if exists postfix_test;
