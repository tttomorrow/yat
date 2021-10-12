-- @testpoint: opengauss关键字current_catalog(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists current_catalog_test;
create table current_catalog_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists current_catalog;
create synonym current_catalog for current_catalog_test;


--关键字带双引号-成功
drop synonym if exists "current_catalog";
create synonym "current_catalog" for current_catalog_test;
insert into "current_catalog" values (1,'ada'),(2, 'bob');
update "current_catalog" set "current_catalog".name='cici' where "current_catalog".id=2;
select * from "current_catalog";

--清理环境
drop synonym "current_catalog";

--关键字带单引号-合理报错
drop synonym if exists 'current_catalog';
create synonym 'current_catalog' for current_catalog_test;
insert into 'current_catalog' values (1,'ada'),(2, 'bob');
update 'current_catalog' set 'current_catalog'.name='cici' where 'current_catalog'.id=2;
select * from 'current_catalog';

--关键字带反引号-合理报错
drop synonym if exists `current_catalog`;
create synonym `current_catalog` for current_catalog_test;
insert into `current_catalog` values (1,'ada'),(2, 'bob');
update `current_catalog` set `current_catalog`.name='cici' where `current_catalog`.id=2;
select * from `current_catalog`;
drop table if exists current_catalog_test;