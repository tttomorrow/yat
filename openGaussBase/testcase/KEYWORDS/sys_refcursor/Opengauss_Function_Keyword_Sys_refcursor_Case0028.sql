-- @testpoint: opengauss关键字sys_refcursor(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists sys_refcursor;
create synonym sys_refcursor for explain_test;
insert into sys_refcursor values (1,'ada'),(2, 'bob');
update sys_refcursor set sys_refcursor.name='cici' where sys_refcursor.id=2;
select * from sys_refcursor;
drop synonym if exists sys_refcursor;

--关键字带双引号-成功
drop synonym if exists "sys_refcursor";
create synonym "sys_refcursor" for explain_test;
drop synonym if exists "sys_refcursor";

--关键字带单引号-合理报错
drop synonym if exists 'sys_refcursor';
create synonym 'sys_refcursor' for explain_test;
insert into 'sys_refcursor' values (1,'ada'),(2, 'bob');
update 'sys_refcursor' set 'sys_refcursor'.name='cici' where 'sys_refcursor'.id=2;
select * from 'sys_refcursor';

--关键字带反引号-合理报错
drop synonym if exists `sys_refcursor`;
create synonym `sys_refcursor` for explain_test;
insert into `sys_refcursor` values (1,'ada'),(2, 'bob');
update `sys_refcursor` set `sys_refcursor`.name='cici' where `sys_refcursor`.id=2;
select * from `sys_refcursor`;

--清理环境
drop table if exists explain_test;