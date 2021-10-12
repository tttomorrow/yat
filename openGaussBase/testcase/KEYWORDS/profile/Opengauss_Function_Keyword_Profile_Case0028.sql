-- @testpoint: opengauss关键字profile(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists profile_test;
create table profile_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists profile;
create synonym profile for profile_test;
insert into profile values (1,'ada'),(2, 'bob');
update profile set profile.name='cici' where profile.id=2;
select * from profile;
drop synonym if exists profile;

--关键字带双引号-成功
drop synonym if exists "profile";
create synonym "profile" for profile_test;
insert into "profile" values (1,'ada'),(2, 'bob');
update "profile" set "profile".name='cici' where "profile".id=2;
select * from "profile";
drop synonym if exists "profile";

--关键字带单引号-合理报错
drop synonym if exists 'profile';

--关键字带反引号-合理报错
drop synonym if exists `profile`;
--清理环境
drop table if exists profile_test;
