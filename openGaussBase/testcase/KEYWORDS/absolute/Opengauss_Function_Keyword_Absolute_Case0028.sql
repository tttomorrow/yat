-- @testpoint: opengauss关键字absolute(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists absolute_test;
create table absolute_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists absolute;
create synonym absolute for absolute_test;
insert into absolute values (1,'ada'),(2, 'bob');
update absolute set absolute.name='cici' where absolute.id=2;
select * from absolute;

--清理环境
drop synonym if exists absolute;

--关键字带双引号-成功
drop synonym if exists "absolute";
create synonym "absolute" for absolute_test;
insert into "absolute" values (1,'ada'),(2, 'bob');
update "absolute" set "absolute".name='cici' where "absolute".id=2;
select * from "absolute";

--清理环境
drop synonym if exists "absolute";

--关键字带单引号-合理报错
drop synonym if exists 'absolute';

--关键字带反引号-合理报错
drop synonym if exists `absolute`;
drop table if exists absolute_test;