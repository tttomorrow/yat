-- @testpoint: opengauss关键字between(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists between_test;
create table between_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists between;
create synonym between for between_test;
insert into between values (1,'ada'),(2, 'bob');
update between set between.name='cici' where between.id=2;
select * from between;

--清理环境
drop synonym if exists between;

--关键字带双引号-成功
drop synonym if exists "between";
create synonym "between" for between_test;
insert into "between" values (1,'ada'),(2, 'bob');
update "between" set "between".name='cici' where "between".id=2;
select * from "between";

--清理环境
drop synonym if exists "between";

--关键字带单引号-合理报错
drop synonym if exists 'between';

--关键字带反引号-合理报错
drop synonym if exists `between`;
drop table if exists between_test;