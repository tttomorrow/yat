-- @testpoint: opengauss关键字or(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists or_test;
create table or_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists or;
create synonym or for or_test;


--关键字带双引号-成功
drop synonym if exists "or";
create synonym "or" for or_test;
insert into "or" values (1,'ada'),(2, 'bob');
update "or" set "or".name='cici' where "or".id=2;
select * from "or";

--清理环境
drop synonym "or";

--关键字带单引号-合理报错
drop synonym if exists 'or';
create synonym 'or' for or_test;
insert into 'or' values (1,'ada'),(2, 'bob');
update 'or' set 'or'.name='cici' where 'or'.id=2;
select * from 'or';

--关键字带反引号-合理报错
drop synonym if exists `or`;
create synonym `or` for or_test;
insert into `or` values (1,'ada'),(2, 'bob');
update `or` set `or`.name='cici' where `or`.id=2;
select * from `or`;
--清理环境
drop table if exists or_test cascade;