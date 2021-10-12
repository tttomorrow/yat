-- @testpoint: opengauss关键字reject(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists reject_test;
create table reject_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists reject;
create synonym reject for reject_test;


--关键字带双引号-成功
drop synonym if exists "reject";
create synonym "reject" for reject_test;
insert into "reject" values (1,'ada'),(2, 'bob');
update "reject" set "reject".name='cici' where "reject".id=2;
select * from "reject";

--清理环境
drop synonym "reject";

--关键字带单引号-合理报错
drop synonym if exists 'reject';
create synonym 'reject' for reject_test;
insert into 'reject' values (1,'ada'),(2, 'bob');
update 'reject' set 'reject'.name='cici' where 'reject'.id=2;
select * from 'reject';

--关键字带反引号-合理报错
drop synonym if exists `reject`;
create synonym `reject` for reject_test;
insert into `reject` values (1,'ada'),(2, 'bob');
update `reject` set `reject`.name='cici' where `reject`.id=2;
select * from `reject`;
drop table if exists reject_test;