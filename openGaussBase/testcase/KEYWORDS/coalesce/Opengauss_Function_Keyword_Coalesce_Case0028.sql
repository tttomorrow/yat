-- @testpoint: opengauss关键字coalesce(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists coalesce_test;
create table coalesce_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists coalesce;
create synonym coalesce for coalesce_test;
insert into coalesce values (1,'ada'),(2, 'bob');
update coalesce set coalesce.name='cici' where coalesce.id=2;
select * from coalesce;

--清理环境
drop synonym if exists coalesce;

--关键字带双引号-成功
drop synonym if exists "coalesce";
create synonym "coalesce" for coalesce_test;
insert into "coalesce" values (1,'ada'),(2, 'bob');
update "coalesce" set "coalesce".name='cici' where "coalesce".id=2;
select * from "coalesce";

--清理环境
drop synonym if exists "coalesce";

--关键字带单引号-合理报错
drop synonym if exists 'coalesce';

--关键字带反引号-合理报错
drop synonym if exists `coalesce`;
drop table if exists coalesce_test;