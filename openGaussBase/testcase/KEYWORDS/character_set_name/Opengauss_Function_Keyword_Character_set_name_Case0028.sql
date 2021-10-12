-- @testpoint: opengauss关键字character_set_name(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists character_set_name_test;
create table character_set_name_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists character_set_name;
create synonym character_set_name for character_set_name_test;
insert into character_set_name values (1,'ada'),(2, 'bob');
update character_set_name set character_set_name.name='cici' where character_set_name.id=2;
select * from character_set_name;

--清理环境
drop synonym if exists character_set_name;

--关键字带双引号-成功
drop synonym if exists "character_set_name";
create synonym "character_set_name" for character_set_name_test;
insert into "character_set_name" values (1,'ada'),(2, 'bob');
update "character_set_name" set "character_set_name".name='cici' where "character_set_name".id=2;
select * from "character_set_name";

--清理环境
drop synonym if exists "character_set_name";

--关键字带单引号-合理报错
drop synonym if exists 'character_set_name';

--关键字带反引号-合理报错
drop synonym if exists `character_set_name`;
drop table if exists character_set_name_test;