-- @testpoint: opengauss关键字nomaxvalue(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists nomaxvalue;
create synonym nomaxvalue for explain_test;
insert into nomaxvalue values (1,'ada'),(2, 'bob');
update nomaxvalue set nomaxvalue.name='cici' where nomaxvalue.id=2;
select * from nomaxvalue;

--关键字带双引号-成功
drop synonym if exists "nomaxvalue";
create synonym "nomaxvalue" for explain_test;


--关键字带单引号-合理报错
drop synonym if exists 'nomaxvalue';
create synonym 'nomaxvalue' for explain_test;
insert into 'nomaxvalue' values (1,'ada'),(2, 'bob');
update 'nomaxvalue' set 'nomaxvalue'.name='cici' where 'nomaxvalue'.id=2;
select * from 'nomaxvalue';

--关键字带反引号-合理报错
drop synonym if exists `nomaxvalue`;
create synonym `nomaxvalue` for explain_test;
insert into `nomaxvalue` values (1,'ada'),(2, 'bob');
update `nomaxvalue` set `nomaxvalue`.name='cici' where `nomaxvalue`.id=2;
select * from `nomaxvalue`;
--清理环境
drop synonym if exists "nomaxvalue";
drop synonym if exists nomaxvalue;
drop table if exists explain_test;