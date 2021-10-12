-- @testpoint: opengauss关键字constraint_schema(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists constraint_schema_test;
create table constraint_schema_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists constraint_schema;
create synonym constraint_schema for constraint_schema_test;
insert into constraint_schema values (1,'ada'),(2, 'bob');
update constraint_schema set constraint_schema.name='cici' where constraint_schema.id=2;
select * from constraint_schema;

--关键字带双引号-成功
drop synonym if exists "constraint_schema";
create synonym "constraint_schema" for constraint_schema_test;


--关键字带单引号-合理报错
drop synonym if exists 'constraint_schema';
create synonym 'constraint_schema' for constraint_schema_test;
insert into 'constraint_schema' values (1,'ada'),(2, 'bob');
update 'constraint_schema' set 'constraint_schema'.name='cici' where 'constraint_schema'.id=2;
select * from 'constraint_schema';

--关键字带反引号-合理报错
drop synonym if exists `constraint_schema`;
create synonym `constraint_schema` for constraint_schema_test;
insert into `constraint_schema` values (1,'ada'),(2, 'bob');
update `constraint_schema` set `constraint_schema`.name='cici' where `constraint_schema`.id=2;
select * from `constraint_schema`;
--清理环境
drop table if exists constraint_schema_test;
drop synonym if exists constraint_schema;
drop synonym if exists "constraint_schema";