-- @testpoint: opengauss关键字trigger_schema(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists trigger_schema;
create synonym trigger_schema for explain_test;
insert into trigger_schema values (1,'ada'),(2, 'bob');
update trigger_schema set trigger_schema.name='cici' where trigger_schema.id=2;
select * from trigger_schema;
drop synonym if exists trigger_schema;

--关键字带双引号-成功
drop synonym if exists "trigger_schema";
create synonym "trigger_schema" for explain_test;
drop synonym if exists "trigger_schema";

--关键字带单引号-合理报错
drop synonym if exists 'trigger_schema';
create synonym 'trigger_schema' for explain_test;
insert into 'trigger_schema' values (1,'ada'),(2, 'bob');
update 'trigger_schema' set 'trigger_schema'.name='cici' where 'trigger_schema'.id=2;
select * from 'trigger_schema';

--关键字带反引号-合理报错
drop synonym if exists `trigger_schema`;
create synonym `trigger_schema` for explain_test;
insert into `trigger_schema` values (1,'ada'),(2, 'bob');
update `trigger_schema` set `trigger_schema`.name='cici' where `trigger_schema`.id=2;
select * from `trigger_schema`;

--清理环境
drop table if exists explain_test;