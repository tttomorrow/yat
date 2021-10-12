-- @testpoint: opengauss关键字collation_schema(非保留)，作为同义词对象名 合理报错


--前置条件
drop table if exists collation_schema_test;
create table collation_schema_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists collation_schema;
create synonym collation_schema for collation_schema_test;
insert into collation_schema values (1,'ada'),(2, 'bob');
update collation_schema set collation_schema.name='cici' where collation_schema.id=2;
select * from collation_schema;
drop synonym if exists collation_schema;
--关键字带双引号-成功
drop synonym if exists "collation_schema";
create synonym "collation_schema" for collation_schema_test;
drop synonym if exists "collation_schema";

--关键字带单引号-合理报错
drop synonym if exists 'collation_schema';
create synonym 'collation_schema' for collation_schema_test;
insert into 'collation_schema' values (1,'ada'),(2, 'bob');
update 'collation_schema' set 'collation_schema'.name='cici' where 'collation_schema'.id=2;
select * from 'collation_schema';

--关键字带反引号-合理报错
drop synonym if exists `collation_schema`;
create synonym `collation_schema` for collation_schema_test;
insert into `collation_schema` values (1,'ada'),(2, 'bob');
update `collation_schema` set `collation_schema`.name='cici' where `collation_schema`.id=2;
select * from `collation_schema`;
drop table if exists collation_schema_test;