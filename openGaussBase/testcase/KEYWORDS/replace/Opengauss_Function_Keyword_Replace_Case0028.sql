-- @testpoint: opengauss关键字replace(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists replace_test;
create table replace_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists replace;
create synonym replace for replace_test;
insert into replace values (1,'ada'),(2, 'bob');
update replace set replace.name='cici' where replace.id=2;
select * from replace;
drop synonym if exists replace;

--关键字带双引号-成功
drop synonym if exists "replace";
create synonym "replace" for replace_test;
insert into "replace" values (1,'ada'),(2, 'bob');
update "replace" set "replace".name='cici' where "replace".id=2;
select * from "replace";
drop synonym if exists "replace";

--关键字带单引号-合理报错
drop synonym if exists 'replace';

--关键字带反引号-合理报错
drop synonym if exists `replace`;
drop table if exists replace_test;