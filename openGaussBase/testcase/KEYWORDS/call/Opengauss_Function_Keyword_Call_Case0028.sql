-- @testpoint: opengauss关键字call(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists call_test;
create table call_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists call;
create synonym call for call_test;
insert into call values (1,'ada'),(2, 'bob');
update call set call.name='cici' where call.id=2;
select * from call;

--清理环境
drop synonym if exists call;

--关键字带双引号-成功
drop synonym if exists "call";
create synonym "call" for call_test;
insert into "call" values (1,'ada'),(2, 'bob');
update "call" set "call".name='cici' where "call".id=2;
select * from "call";

--清理环境
drop synonym if exists "call";

--关键字带单引号-合理报错
drop synonym if exists 'call';

--关键字带反引号-合理报错
drop synonym if exists `call`;
drop table if exists call_test;