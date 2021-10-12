-- @testpoint: opengauss关键字clean(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists clean_test;
create table clean_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists clean;
create synonym clean for clean_test;
insert into clean values (1,'ada'),(2, 'bob');
update clean set clean.name='cici' where clean.id=2;
select * from clean;

--清理环境
drop synonym if exists clean;

--关键字带双引号-成功
drop synonym if exists "clean";
create synonym "clean" for clean_test;
insert into "clean" values (1,'ada'),(2, 'bob');
update "clean" set "clean".name='cici' where "clean".id=2;
select * from "clean";

--清理环境
drop synonym if exists "clean";

--关键字带单引号-合理报错
drop synonym if exists 'clean';

--关键字带反引号-合理报错
drop synonym if exists `clean`;
drop table if exists clean_test;