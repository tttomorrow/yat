-- @testpoint: opengauss关键字release(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists release_test;
create table release_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists release;
create synonym release for release_test;
insert into release values (1,'ada'),(2, 'bob');
update release set release.name='cici' where release.id=2;
select * from release;
drop synonym if exists release;

--关键字带双引号-成功
drop synonym if exists "release";
create synonym "release" for release_test;
insert into "release" values (1,'ada'),(2, 'bob');
update "release" set "release".name='cici' where "release".id=2;
select * from "release";
drop synonym if exists "release";

--关键字带单引号-合理报错
drop synonym if exists 'release';

--关键字带反引号-合理报错
drop synonym if exists `release`;
drop table if exists release_test;