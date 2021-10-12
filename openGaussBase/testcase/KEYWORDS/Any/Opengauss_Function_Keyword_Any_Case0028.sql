-- @testpoint: opengauss关键字Any(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists Any_test;
create table Any_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists Any;
create synonym Any for Any_test;


--关键字带双引号-成功
drop synonym if exists "Any";
create synonym "Any" for Any_test;
insert into "Any" values (1,'ada'),(2, 'bob');
update "Any" set "Any".name='cici' where "Any".id=2;
select * from "Any";

--清理环境
drop synonym "Any";

--关键字带单引号-合理报错
drop synonym if exists 'Any';
create synonym 'Any' for Any_test;
insert into 'Any' values (1,'ada'),(2, 'bob');
update 'Any' set 'Any'.name='cici' where 'Any'.id=2;
select * from 'Any';

--关键字带反引号-合理报错
drop synonym if exists `Any`;
create synonym `Any` for Any_test;
insert into `Any` values (1,'ada'),(2, 'bob');
update `Any` set `Any`.name='cici' where `Any`.id=2;
select * from `Any`;
drop table if exists Any_test;