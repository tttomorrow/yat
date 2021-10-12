-- @testpoint: opengauss关键字natural(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists natural_test;
create table natural_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists natural;
create synonym natural for natural_test;


--关键字带双引号-成功
drop synonym if exists "natural";
create synonym "natural" for natural_test;
insert into "natural" values (1,'ada'),(2, 'bob');
update "natural" set "natural".name='cici' where "natural".id=2;
select * from "natural";

--清理环境
drop synonym "natural";

--关键字带单引号-合理报错
drop synonym if exists 'natural';
create synonym 'natural' for natural_test;
insert into 'natural' values (1,'ada'),(2, 'bob');
update 'natural' set 'natural'.name='cici' where 'natural'.id=2;
select * from 'natural';

--关键字带反引号-合理报错
drop synonym if exists `natural`;
create synonym `natural` for natural_test;
insert into `natural` values (1,'ada'),(2, 'bob');
update `natural` set `natural`.name='cici' where `natural`.id=2;
select * from `natural`;
--清理环境
drop synonym if exists "natural";
drop table if exists natural_test;