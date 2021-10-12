-- @testpoint: opengauss关键字character(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists character_test;
create table character_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists character;
create synonym character for character_test;
insert into character values (1,'ada'),(2, 'bob');
update character set character.name='cici' where character.id=2;
select * from character;

--清理环境
drop synonym if exists character;

--关键字带双引号-成功
drop synonym if exists "character";
create synonym "character" for character_test;
insert into "character" values (1,'ada'),(2, 'bob');
update "character" set "character".name='cici' where "character".id=2;
select * from "character";

--清理环境
drop synonym if exists "character";

--关键字带单引号-合理报错
drop synonym if exists 'character';

--关键字带反引号-合理报错
drop synonym if exists `character`;
drop table if exists character_test;