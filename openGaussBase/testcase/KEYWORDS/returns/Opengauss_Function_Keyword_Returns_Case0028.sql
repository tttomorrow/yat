-- @testpoint: opengauss关键字returns(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists returns_test;
create table returns_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists returns;
create synonym returns for returns_test;
insert into returns values (1,'ada'),(2, 'bob');
update returns set returns.name='cici' where returns.id=2;
select * from returns;

--清理环境
drop synonym if exists returns;

--关键字带双引号-成功
drop synonym if exists "returns";
create synonym "returns" for returns_test;
insert into "returns" values (1,'ada'),(2, 'bob');
update "returns" set "returns".name='cici' where "returns".id=2;
select * from "returns";

--清理环境
drop synonym if exists "returns";

--关键字带单引号-合理报错
drop synonym if exists 'returns';

--关键字带反引号-合理报错
drop synonym if exists `returns`;
drop table if exists returns_test;