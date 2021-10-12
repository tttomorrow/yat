-- @testpoint: opengauss关键字like(保留)，作为同义词对象名 合理报错


--前置条件
drop table if exists like_test;
create table like_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists like;
create synonym like for like_test;


--关键字带双引号-成功
drop synonym if exists "like";
create synonym "like" for like_test;
insert into "like" values (1,'ada'),(2, 'bob');
update "like" set "like".name='cici' where "like".id=2;
select * from "like";

--清理环境
drop synonym "like";

--关键字带单引号-合理报错
drop synonym if exists 'like';
create synonym 'like' for like_test;
insert into 'like' values (1,'ada'),(2, 'bob');
update 'like' set 'like'.name='cici' where 'like'.id=2;
select * from 'like';

--关键字带反引号-合理报错
drop synonym if exists `like`;
create synonym `like` for like_test;
insert into `like` values (1,'ada'),(2, 'bob');
update `like` set `like`.name='cici' where `like`.id=2;
select * from `like`;
--清理环境
drop table if exists like_test cascade;