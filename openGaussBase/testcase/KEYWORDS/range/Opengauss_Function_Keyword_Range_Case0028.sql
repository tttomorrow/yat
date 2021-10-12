-- @testpoint: opengauss关键字range(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists range_test;
create table range_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists range;
create synonym range for range_test;
insert into range values (1,'ada'),(2, 'bob');
update range set range.name='cici' where range.id=2;
select * from range;
drop synonym if exists range;

--关键字带双引号-成功
drop synonym if exists "range";
create synonym "range" for range_test;
insert into "range" values (1,'ada'),(2, 'bob');
update "range" set "range".name='cici' where "range".id=2;
select * from "range";
drop synonym if exists "range";

--关键字带单引号-合理报错
drop synonym if exists 'range';

--关键字带反引号-合理报错
drop synonym if exists `range`;
--清理环境
drop table if exists range_test;