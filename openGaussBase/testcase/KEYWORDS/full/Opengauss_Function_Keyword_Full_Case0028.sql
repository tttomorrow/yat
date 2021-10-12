-- @testpoint: opengauss关键字full(保留)，作为同义词对象名，部分测试点合理报错

--前置条件
drop table if exists full_test;
create table full_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists full;
create synonym full for full_test;

--关键字带双引号-成功
drop synonym if exists "full";
create synonym "full" for full_test;
insert into "full" values (1,'ada'),(2, 'bob');
update "full" set "full".name='cici' where "full".id=2;
select * from "full";

--清理环境
drop synonym "full";

--关键字带单引号-合理报错
drop synonym if exists 'full';
create synonym 'full' for full_test;
insert into 'full' values (1,'ada'),(2, 'bob');
update 'full' set 'full'.name='cici' where 'full'.id=2;
select * from 'full';

--关键字带反引号-合理报错
drop synonym if exists `full`;
create synonym `full` for full_test;
insert into `full` values (1,'ada'),(2, 'bob');
update `full` set `full`.name='cici' where `full`.id=2;
select * from `full`;

--清理环境
drop table if exists full_test;