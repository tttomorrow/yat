-- @testpoint: opengauss关键字constraint_catalog(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists constraint_catalog_test;
create table constraint_catalog_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists constraint_catalog;
create synonym constraint_catalog for constraint_catalog_test;
insert into constraint_catalog values (1,'ada'),(2, 'bob');
update constraint_catalog set constraint_catalog.name='cici' where constraint_catalog.id=2;
select * from constraint_catalog;

--关键字带双引号-成功
drop synonym if exists "constraint_catalog";
create synonym "constraint_catalog" for constraint_catalog_test;


--关键字带单引号-合理报错
drop synonym if exists 'constraint_catalog';
create synonym 'constraint_catalog' for constraint_catalog_test;
insert into 'constraint_catalog' values (1,'ada'),(2, 'bob');
update 'constraint_catalog' set 'constraint_catalog'.name='cici' where 'constraint_catalog'.id=2;
select * from 'constraint_catalog';

--关键字带反引号-合理报错
drop synonym if exists `constraint_catalog`;
create synonym `constraint_catalog` for constraint_catalog_test;
insert into `constraint_catalog` values (1,'ada'),(2, 'bob');
update `constraint_catalog` set `constraint_catalog`.name='cici' where `constraint_catalog`.id=2;
select * from `constraint_catalog`;

--清理环境
drop synonym if exists constraint_catalog;
drop synonym if exists "constraint_catalog";
drop table if exists constraint_catalog_test;