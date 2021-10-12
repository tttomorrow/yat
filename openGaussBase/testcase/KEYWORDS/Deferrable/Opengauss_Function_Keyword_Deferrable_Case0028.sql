-- @testpoint: opengauss关键字deferrable(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists deferrable_test;
create table deferrable_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists deferrable;
create synonym deferrable for deferrable_test;


--关键字带双引号-成功
drop synonym if exists "deferrable";
create synonym "deferrable" for deferrable_test;
insert into "deferrable" values (1,'ada'),(2, 'bob');
update "deferrable" set "deferrable".name='cici' where "deferrable".id=2;
select * from "deferrable";
drop synonym "deferrable";
--关键字带单引号-合理报错
drop synonym if exists 'deferrable';
create synonym 'deferrable' for deferrable_test;
insert into 'deferrable' values (1,'ada'),(2, 'bob');
update 'deferrable' set 'deferrable'.name='cici' where 'deferrable'.id=2;
select * from 'deferrable';

--关键字带反引号-合理报错
drop synonym if exists `deferrable`;
create synonym `deferrable` for deferrable_test;
insert into `deferrable` values (1,'ada'),(2, 'bob');
update `deferrable` set `deferrable`.name='cici' where `deferrable`.id=2;
select * from `deferrable`;
drop table if exists deferrable_test;