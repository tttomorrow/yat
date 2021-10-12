-- @testpoint: opengauss关键字access(非保留)，作为同义词对象名,部分测试点合理报错
--前置条件
drop table if exists access_test;
create table access_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists access;
create synonym access for access_test;
insert into access values (1,'ada'),(2, 'bob');
update access set access.name='cici' where access.id=2;
select * from access;

--清理环境
drop synonym if exists access;

--关键字带双引号-成功
drop synonym if exists "access";
create synonym "access" for access_test;
insert into "access" values (1,'ada'),(2, 'bob');
update "access" set "access".name='cici' where "access".id=2;
select * from "access";

--清理环境
drop synonym if exists "access";
drop table access_test;

--关键字带单引号-合理报错
drop synonym if exists 'access';

--关键字带反引号-合理报错
drop synonym if exists `access`;
