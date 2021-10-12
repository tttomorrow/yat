-- @testpoint: opengauss关键字false(保留)，作为同义词对象名，部分测试点合理报错

--前置条件
drop table if exists false_test;
create table false_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists false;
create synonym false for false_test;


--关键字带双引号-成功
drop synonym if exists "false";
create synonym "false" for false_test;
insert into "false" values (1,'ada'),(2, 'bob');
update "false" set "false".name='cici' where "false".id=2;
select * from "false";
drop synonym "false";
--关键字带单引号-合理报错
drop synonym if exists 'false';
create synonym 'false' for false_test;
insert into 'false' values (1,'ada'),(2, 'bob');
update 'false' set 'false'.name='cici' where 'false'.id=2;
select * from 'false';

--关键字带反引号-合理报错
drop synonym if exists `false`;
create synonym `false` for false_test;
insert into `false` values (1,'ada'),(2, 'bob');
update `false` set `false`.name='cici' where `false`.id=2;
select * from `false`;
drop table if exists false_test;