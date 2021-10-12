-- @testpoint: opengauss关键字prior(非保留)，作为同义词对象名,合理报错


--前置条件
drop table if exists prior_test;
create table prior_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists prior;
create synonym prior for prior_test;
insert into prior values (1,'ada'),(2, 'bob');
update prior set prior.name='cici' where prior.id=2;
select * from prior;

--关键字带双引号-成功
drop synonym if exists "prior";
create synonym "prior" for prior_test;
insert into "prior" values (1,'ada'),(2, 'bob');
update "prior" set "prior".name='cici' where "prior".id=2;
select * from "prior";

--关键字带单引号-合理报错
drop synonym if exists 'prior';
create synonym 'prior' for prior_test;

--关键字带反引号-合理报错
drop synonym if exists `prior`;
create synonym `prior` for prior_test;

--清理环境
drop synonym if exists prior;
drop synonym if exists "prior";
drop table if exists prior_test;