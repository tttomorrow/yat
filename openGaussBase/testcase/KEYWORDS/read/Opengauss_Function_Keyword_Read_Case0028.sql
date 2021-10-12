-- @testpoint: opengauss关键字read(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists read_test;
create table read_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists read;
create synonym read for read_test;
insert into read values (1,'ada'),(2, 'bob');
update read set read.name='cici' where read.id=2;
select * from read;
drop synonym if exists read;

--关键字带双引号-成功
drop synonym if exists "read";
create synonym "read" for read_test;
insert into "read" values (1,'ada'),(2, 'bob');
update "read" set "read".name='cici' where "read".id=2;
select * from "read";
drop synonym if exists "read";

--关键字带单引号-合理报错
drop synonym if exists 'read';

--关键字带反引号-合理报错
drop synonym if exists `read`;
--清理环境
drop table if exists read_test;