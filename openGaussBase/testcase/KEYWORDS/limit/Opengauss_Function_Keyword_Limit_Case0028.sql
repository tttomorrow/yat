-- @testpoint: opengauss关键字limit(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists limit_test;
create table limit_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists limit;
create synonym limit for limit_test;


--关键字带双引号-成功
drop synonym if exists "limit";
create synonym "limit" for limit_test;
insert into "limit" values (1,'ada'),(2, 'bob');
update "limit" set "limit".name='cici' where "limit".id=2;
select * from "limit";

--清理环境
drop synonym "limit";

--关键字带单引号-合理报错
drop synonym if exists 'limit';
create synonym 'limit' for limit_test;
insert into 'limit' values (1,'ada'),(2, 'bob');
update 'limit' set 'limit'.name='cici' where 'limit'.id=2;
select * from 'limit';

--关键字带反引号-合理报错
drop synonym if exists `limit`;
create synonym `limit` for limit_test;
insert into `limit` values (1,'ada'),(2, 'bob');
update `limit` set `limit`.name='cici' where `limit`.id=2;
select * from `limit`;
--清理环境
drop table if exists limit_test cascade;