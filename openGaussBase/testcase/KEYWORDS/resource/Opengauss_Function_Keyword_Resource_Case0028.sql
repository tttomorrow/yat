-- @testpoint: opengauss关键字resource(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists resource_test;
create table resource_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists resource;
create synonym resource for resource_test;
insert into resource values (1,'ada'),(2, 'bob');
update resource set resource.name='cici' where resource.id=2;
select * from resource;
drop synonym if exists resource;

--关键字带双引号-成功
drop synonym if exists "resource";
create synonym "resource" for resource_test;
insert into "resource" values (1,'ada'),(2, 'bob');
update "resource" set "resource".name='cici' where "resource".id=2;
select * from "resource";
drop synonym if exists "resource";

--关键字带单引号-合理报错
drop synonym if exists 'resource';

--关键字带反引号-合理报错
drop synonym if exists `resource`;
drop table if exists resource_test;