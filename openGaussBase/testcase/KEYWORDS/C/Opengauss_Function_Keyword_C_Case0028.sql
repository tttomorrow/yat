-- @testpoint: opengauss关键字c(非保留)，作为同义词对象名,部分测试点合理报错
--前置条件
drop table if exists c_test;
create table c_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists c;
create synonym c for c_test;
insert into c values (1,'ada'),(2, 'bob');
update c set c.name='cici' where c.id=2;
select * from c;

--清理环境
drop synonym if exists c;

--关键字带双引号-成功
drop synonym if exists "c";
create synonym "c" for c_test;
insert into "c" values (1,'ada'),(2, 'bob');
update "c" set "c".name='cici' where "c".id=2;
select * from "c";

--清理环境
drop synonym if exists "c";

--关键字带单引号-合理报错
drop synonym if exists 'c';

--关键字带反引号-合理报错
drop synonym if exists `c`;
drop table if exists c_test;