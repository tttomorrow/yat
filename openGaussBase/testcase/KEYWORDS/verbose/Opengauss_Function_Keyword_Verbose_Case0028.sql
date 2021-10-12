-- @testpoint: opengauss关键字verbose(保留)，作为同义词对象名 合理报错


--前置条件
drop table if exists verbose_test;
create table verbose_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists verbose;
create synonym verbose for verbose_test;


--关键字带双引号-成功
drop synonym if exists "verbose";
create synonym "verbose" for verbose_test;
insert into "verbose" values (1,'ada'),(2, 'bob');
update "verbose" set "verbose".name='cici' where "verbose".id=2;
select * from "verbose";

--清理环境
drop synonym "verbose";

--关键字带单引号-合理报错
drop synonym if exists 'verbose';
create synonym 'verbose' for verbose_test;
insert into 'verbose' values (1,'ada'),(2, 'bob');
update 'verbose' set 'verbose'.name='cici' where 'verbose'.id=2;
select * from 'verbose';

--关键字带反引号-合理报错
drop synonym if exists `verbose`;
create synonym `verbose` for verbose_test;
insert into `verbose` values (1,'ada'),(2, 'bob');
update `verbose` set `verbose`.name='cici' where `verbose`.id=2;
select * from `verbose`;
drop table if exists verbose_test;