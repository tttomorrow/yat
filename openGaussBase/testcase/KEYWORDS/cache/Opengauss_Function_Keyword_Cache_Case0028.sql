-- @testpoint: opengauss关键字cache(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists cache_test;
create table cache_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists cache;
create synonym cache for cache_test;
insert into cache values (1,'ada'),(2, 'bob');
update cache set cache.name='cici' where cache.id=2;
select * from cache;

--清理环境
drop synonym if exists cache;

--关键字带双引号-成功
drop synonym if exists "cache";
create synonym "cache" for cache_test;
insert into "cache" values (1,'ada'),(2, 'bob');
update "cache" set "cache".name='cici' where "cache".id=2;
select * from "cache";

--清理环境
drop synonym if exists "cache";

--关键字带单引号-合理报错
drop synonym if exists 'cache';

--关键字带反引号-合理报错
drop synonym if exists `cache`;
drop table if exists cache_test;