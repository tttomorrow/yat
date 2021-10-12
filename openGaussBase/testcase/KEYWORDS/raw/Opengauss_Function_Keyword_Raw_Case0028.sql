-- @testpoint: opengauss关键字raw(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists raw_test;
create table raw_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists raw;
create synonym raw for raw_test;
insert into raw values (1,'ada'),(2, 'bob');
update raw set raw.name='cici' where raw.id=2;
select * from raw;
drop synonym if exists raw;

--关键字带双引号-成功
drop synonym if exists "raw";
create synonym "raw" for raw_test;
insert into "raw" values (1,'ada'),(2, 'bob');
update "raw" set "raw".name='cici' where "raw".id=2;
select * from "raw";
drop synonym if exists "raw";

--关键字带单引号-合理报错
drop synonym if exists 'raw';

--关键字带反引号-合理报错
drop synonym if exists `raw`;
--清理环境
drop table if exists raw_test;