-- @testpoint: opengauss关键字reassign(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists reassign_test;
create table reassign_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists reassign;
create synonym reassign for reassign_test;
insert into reassign values (1,'ada'),(2, 'bob');
update reassign set reassign.name='cici' where reassign.id=2;
select * from reassign;
drop synonym if exists reassign;

--关键字带双引号-成功
drop synonym if exists "reassign";
create synonym "reassign" for reassign_test;
insert into "reassign" values (1,'ada'),(2, 'bob');
update "reassign" set "reassign".name='cici' where "reassign".id=2;
select * from "reassign";
drop synonym if exists "reassign";

--关键字带单引号-合理报错
drop synonym if exists 'reassign';

--关键字带反引号-合理报错
drop synonym if exists `reassign`;
--清理环境
drop table if exists reassign_test;