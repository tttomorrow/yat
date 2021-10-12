-- @testpoint: opengauss关键字reloptions(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists reloptions_test;
create table reloptions_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists reloptions;
create synonym reloptions for reloptions_test;
insert into reloptions values (1,'ada'),(2, 'bob');
update reloptions set reloptions.name='cici' where reloptions.id=2;
select * from reloptions;
drop synonym if exists reloptions;

--关键字带双引号-成功
drop synonym if exists "reloptions";
create synonym "reloptions" for reloptions_test;
insert into "reloptions" values (1,'ada'),(2, 'bob');
update "reloptions" set "reloptions".name='cici' where "reloptions".id=2;
select * from "reloptions";
drop synonym if exists "reloptions";

--关键字带单引号-合理报错
drop synonym if exists 'reloptions';

--关键字带反引号-合理报错
drop synonym if exists `reloptions`;
drop table if exists reloptions_test;