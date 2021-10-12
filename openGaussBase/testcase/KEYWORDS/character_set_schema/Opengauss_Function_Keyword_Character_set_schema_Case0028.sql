-- @testpoint: opengauss关键字character_set_schema(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists character_set_schema_test;
create table character_set_schema_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists character_set_schema;
create synonym character_set_schema for character_set_schema_test;
insert into character_set_schema values (1,'ada'),(2, 'bob');
update character_set_schema set character_set_schema.name='cici' where character_set_schema.id=2;
select * from character_set_schema;

--清理环境
drop synonym if exists character_set_schema;

--关键字带双引号-成功
drop synonym if exists "character_set_schema";
create synonym "character_set_schema" for character_set_schema_test;
insert into "character_set_schema" values (1,'ada'),(2, 'bob');
update "character_set_schema" set "character_set_schema".name='cici' where "character_set_schema".id=2;
select * from "character_set_schema";

--清理环境
drop synonym if exists "character_set_schema";

--关键字带单引号-合理报错
drop synonym if exists 'character_set_schema';

--关键字带反引号-合理报错
drop synonym if exists `character_set_schema`;
drop table if exists character_set_schema_test;