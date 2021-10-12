-- @testpoint: opengauss关键字routine_schema(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists routine_schema;
create synonym routine_schema for explain_test;
insert into routine_schema values (1,'ada'),(2, 'bob');
update routine_schema set routine_schema.name='cici' where routine_schema.id=2;
select * from routine_schema;
drop synonym if exists routine_schema;

--关键字带双引号-成功
drop synonym if exists "routine_schema";
create synonym "routine_schema" for explain_test;
drop synonym if exists "routine_schema";

--关键字带单引号-合理报错
drop synonym if exists 'routine_schema';
create synonym 'routine_schema' for explain_test;
insert into 'routine_schema' values (1,'ada'),(2, 'bob');
update 'routine_schema' set 'routine_schema'.name='cici' where 'routine_schema'.id=2;
select * from 'routine_schema';

--关键字带反引号-合理报错
drop synonym if exists `routine_schema`;
create synonym `routine_schema` for explain_test;
insert into `routine_schema` values (1,'ada'),(2, 'bob');
update `routine_schema` set `routine_schema`.name='cici' where `routine_schema`.id=2;
select * from `routine_schema`;
drop table if exists explain_test;