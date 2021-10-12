-- @testpoint: opengauss关键字current_schema(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists current_schema_test;
create table current_schema_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists current_schema;
create synonym current_schema for current_schema_test;


--关键字带双引号-成功
drop synonym if exists "current_schema";
create synonym "current_schema" for current_schema_test;
insert into "current_schema" values (1,'ada'),(2, 'bob');
update "current_schema" set "current_schema".name='cici' where "current_schema".id=2;
select * from "current_schema";

--清理环境
drop synonym "current_schema";

--关键字带单引号-合理报错
drop synonym if exists 'current_schema';
create synonym 'current_schema' for current_schema_test;
insert into 'current_schema' values (1,'ada'),(2, 'bob');
update 'current_schema' set 'current_schema'.name='cici' where 'current_schema'.id=2;
select * from 'current_schema';

--关键字带反引号-合理报错
drop synonym if exists `current_schema`;
create synonym `current_schema` for current_schema_test;
insert into `current_schema` values (1,'ada'),(2, 'bob');
update `current_schema` set `current_schema`.name='cici' where `current_schema`.id=2;
select * from `current_schema`;
drop table if exists current_schema_test;