-- @testpoint: opengauss关键字null(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists null_test;
create table null_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists null;
create synonym null for null_test;


--关键字带双引号-成功
drop synonym if exists "null";
create synonym "null" for null_test;
insert into "null" values (1,'ada'),(2, 'bob');
update "null" set "null".name='cici' where "null".id=2;
select * from "null";

--清理环境
drop synonym "null";

--关键字带单引号-合理报错
drop synonym if exists 'null';
create synonym 'null' for null_test;
insert into 'null' values (1,'ada'),(2, 'bob');
update 'null' set 'null'.name='cici' where 'null'.id=2;
select * from 'null';

--关键字带反引号-合理报错
drop synonym if exists `null`;
create synonym `null` for null_test;
insert into `null` values (1,'ada'),(2, 'bob');
update `null` set `null`.name='cici' where `null`.id=2;
select * from `null`;
--清理环境
drop table if exists null_test cascade;