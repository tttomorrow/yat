-- @testpoint: opengauss关键字prefix(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists prefix_test;
create table prefix_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists prefix;
create synonym prefix for prefix_test;
insert into prefix values (1,'ada'),(2, 'bob');
update prefix set prefix.name='cici' where prefix.id=2;
select * from prefix;

--关键字带双引号-成功
drop synonym if exists "prefix";
create synonym "prefix" for prefix_test;
insert into "prefix" values (1,'ada'),(2, 'bob');
update "prefix" set "prefix".name='cici' where "prefix".id=2;
select * from "prefix";

--关键字带单引号-合理报错
drop synonym if exists 'prefix';
create synonym 'prefix' for prefix_test;

--关键字带反引号-合理报错
drop synonym if exists `prefix`;
create synonym `prefix` for prefix_test;
--清理环境
drop synonym if exists "prefix";
drop synonym if exists prefix;
drop table if exists prefix_test;
