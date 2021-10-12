-- @testpoint: opengauss关键字preferred(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists preferred_test;
create table preferred_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists preferred;
create synonym preferred for preferred_test;
insert into preferred values (1,'ada'),(2, 'bob');
update preferred set preferred.name='cici' where preferred.id=2;
select * from preferred;

--关键字带双引号-成功
drop synonym if exists "preferred";
create synonym "preferred" for preferred_test;
insert into "preferred" values (1,'ada'),(2, 'bob');
update "preferred" set "preferred".name='cici' where "preferred".id=2;
select * from "preferred";

--关键字带单引号-合理报错
drop synonym if exists 'preferred';
create synonym 'preferred' for preferred_test;

--关键字带反引号-合理报错
drop synonym if exists `preferred`;
create synonym `preferred` for preferred_test;
--清理环境
drop synonym if exists "preferred";
drop synonym if exists preferred;
drop table if exists preferred_test;
