-- @testpoint: opengauss关键字collation_catalog(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists collation_catalog_test;
create table collation_catalog_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists collation_catalog;
create synonym collation_catalog for collation_catalog_test;
insert into collation_catalog values (1,'ada'),(2, 'bob');
update collation_catalog set collation_catalog.name='cici' where collation_catalog.id=2;
select * from collation_catalog;
drop synonym if exists collation_catalog;
--关键字带双引号-成功
drop synonym if exists "collation_catalog";
create synonym "collation_catalog" for collation_catalog_test;
drop synonym if exists "collation_catalog";

--关键字带单引号-合理报错
drop synonym if exists 'collation_catalog';
create synonym 'collation_catalog' for collation_catalog_test;
insert into 'collation_catalog' values (1,'ada'),(2, 'bob');
update 'collation_catalog' set 'collation_catalog'.name='cici' where 'collation_catalog'.id=2;
select * from 'collation_catalog';

--关键字带反引号-合理报错
drop synonym if exists `collation_catalog`;
create synonym `collation_catalog` for collation_catalog_test;
insert into `collation_catalog` values (1,'ada'),(2, 'bob');
update `collation_catalog` set `collation_catalog`.name='cici' where `collation_catalog`.id=2;
select * from `collation_catalog`;
drop table if exists collation_catalog_test;