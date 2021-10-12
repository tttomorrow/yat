-- @testpoint: opengauss关键字catalog_name(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists catalog_name_test;
create table catalog_name_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists catalog_name;
create synonym catalog_name for catalog_name_test;
insert into catalog_name values (1,'ada'),(2, 'bob');
update catalog_name set catalog_name.name='cici' where catalog_name.id=2;
select * from catalog_name;

--清理环境
drop synonym if exists catalog_name;

--关键字带双引号-成功
drop synonym if exists "catalog_name";
create synonym "catalog_name" for catalog_name_test;
insert into "catalog_name" values (1,'ada'),(2, 'bob');
update "catalog_name" set "catalog_name".name='cici' where "catalog_name".id=2;
select * from "catalog_name";

--清理环境
drop synonym if exists "catalog_name";

--关键字带单引号-合理报错
drop synonym if exists 'catalog_name';

--关键字带反引号-合理报错
drop synonym if exists `catalog_name`;
drop table if exists catalog_name_test;