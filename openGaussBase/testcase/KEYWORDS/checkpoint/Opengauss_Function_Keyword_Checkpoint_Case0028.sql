-- @testpoint: opengauss关键字checkpoint(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists checkpoint_test;
create table checkpoint_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists checkpoint;
create synonym checkpoint for checkpoint_test;
insert into checkpoint values (1,'ada'),(2, 'bob');
update checkpoint set checkpoint.name='cici' where checkpoint.id=2;
select * from checkpoint;

--清理环境
drop synonym if exists checkpoint;

--关键字带双引号-成功
drop synonym if exists "checkpoint";
create synonym "checkpoint" for checkpoint_test;
insert into "checkpoint" values (1,'ada'),(2, 'bob');
update "checkpoint" set "checkpoint".name='cici' where "checkpoint".id=2;
select * from "checkpoint";

--清理环境
drop synonym if exists "checkpoint";

--关键字带单引号-合理报错
drop synonym if exists 'checkpoint';

--关键字带反引号-合理报错
drop synonym if exists `checkpoint`;
drop table if exists checkpoint_test;