-- @testpoint: opengauss关键字octet_length(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists octet_length;
create synonym octet_length for explain_test;
insert into octet_length values (1,'ada'),(2, 'bob');
update octet_length set octet_length.name='cici' where octet_length.id=2;
select * from octet_length;

--关键字带双引号-成功
drop synonym if exists "octet_length";
create synonym "octet_length" for explain_test;


--关键字带单引号-合理报错
drop synonym if exists 'octet_length';
create synonym 'octet_length' for explain_test;
insert into 'octet_length' values (1,'ada'),(2, 'bob');
update 'octet_length' set 'octet_length'.name='cici' where 'octet_length'.id=2;
select * from 'octet_length';

--关键字带反引号-合理报错
drop synonym if exists `octet_length`;
create synonym `octet_length` for explain_test;
insert into `octet_length` values (1,'ada'),(2, 'bob');
update `octet_length` set `octet_length`.name='cici' where `octet_length`.id=2;
select * from `octet_length`;
--清理环境
drop synonym if exists "octet_length";
drop synonym if exists octet_length;
drop table if exists explain_test;