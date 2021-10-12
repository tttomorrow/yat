-- @testpoint: opengauss关键字Language(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists Language;
create synonym Language for explain_test;
insert into Language values (1,'ada'),(2, 'bob');
update Language set Language.name='cici' where Language.id=2;
select * from Language;

--关键字带双引号-成功
drop synonym if exists "Language";
create synonym "Language" for explain_test;


--关键字带单引号-合理报错
drop synonym if exists 'Language';
create synonym 'Language' for explain_test;
insert into 'Language' values (1,'ada'),(2, 'bob');
update 'Language' set 'Language'.name='cici' where 'Language'.id=2;
select * from 'Language';

--关键字带反引号-合理报错
drop synonym if exists `Language`;
create synonym `Language` for explain_test;
insert into `Language` values (1,'ada'),(2, 'bob');
update `Language` set `Language`.name='cici' where `Language`.id=2;
select * from `Language`;
--清理环境
drop synonym if exists language;
drop synonym if exists "Language";
drop table if exists explain_test;