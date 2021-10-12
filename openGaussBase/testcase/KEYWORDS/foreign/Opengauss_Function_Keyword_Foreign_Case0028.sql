-- @testpoint: opengauss关键字foreign(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists foreign_test;
create table foreign_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists foreign;
create synonym foreign for foreign_test;


--关键字带双引号-成功
drop synonym if exists "foreign";
create synonym "foreign" for foreign_test;
insert into "foreign" values (1,'ada'),(2, 'bob');
update "foreign" set "foreign".name='cici' where "foreign".id=2;
select * from "foreign";

--清理环境
drop synonym "foreign";

--关键字带单引号-合理报错
drop synonym if exists 'foreign';
create synonym 'foreign' for foreign_test;
insert into 'foreign' values (1,'ada'),(2, 'bob');
update 'foreign' set 'foreign'.name='cici' where 'foreign'.id=2;
select * from 'foreign';

--关键字带反引号-合理报错
drop synonym if exists `foreign`;
create synonym `foreign` for foreign_test;
insert into `foreign` values (1,'ada'),(2, 'bob');
update `foreign` set `foreign`.name='cici' where `foreign`.id=2;
select * from `foreign`;
drop table if exists foreign_test;