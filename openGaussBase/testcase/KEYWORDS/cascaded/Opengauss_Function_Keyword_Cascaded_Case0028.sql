-- @testpoint: opengauss关键字cascaded(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists cascaded_test;
create table cascaded_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists cascaded;
create synonym cascaded for cascaded_test;
insert into cascaded values (1,'ada'),(2, 'bob');
update cascaded set cascaded.name='cici' where cascaded.id=2;
select * from cascaded;

--清理环境
drop synonym if exists cascaded;

--关键字带双引号-成功
drop synonym if exists "cascaded";
create synonym "cascaded" for cascaded_test;
insert into "cascaded" values (1,'ada'),(2, 'bob');
update "cascaded" set "cascaded".name='cici' where "cascaded".id=2;
select * from "cascaded";

--清理环境
drop synonym if exists "cascaded";

--关键字带单引号-合理报错
drop synonym if exists 'cascaded';

--关键字带反引号-合理报错
drop synonym if exists `cascaded`;
drop table if exists cascaded_test;