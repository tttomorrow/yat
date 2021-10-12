-- @testpoint: opengauss关键字trigger_catalog(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists trigger_catalog;
create synonym trigger_catalog for explain_test;
insert into trigger_catalog values (1,'ada'),(2, 'bob');
update trigger_catalog set trigger_catalog.name='cici' where trigger_catalog.id=2;
select * from trigger_catalog;
drop synonym if exists trigger_catalog;

--关键字带双引号-成功
drop synonym if exists "trigger_catalog";
create synonym "trigger_catalog" for explain_test;
drop synonym if exists "trigger_catalog";

--关键字带单引号-合理报错
drop synonym if exists 'trigger_catalog';
create synonym 'trigger_catalog' for explain_test;
insert into 'trigger_catalog' values (1,'ada'),(2, 'bob');
update 'trigger_catalog' set 'trigger_catalog'.name='cici' where 'trigger_catalog'.id=2;
select * from 'trigger_catalog';

--关键字带反引号-合理报错
drop synonym if exists `trigger_catalog`;
create synonym `trigger_catalog` for explain_test;
insert into `trigger_catalog` values (1,'ada'),(2, 'bob');
update `trigger_catalog` set `trigger_catalog`.name='cici' where `trigger_catalog`.id=2;
select * from `trigger_catalog`;

--清理环境
drop table if exists explain_test;