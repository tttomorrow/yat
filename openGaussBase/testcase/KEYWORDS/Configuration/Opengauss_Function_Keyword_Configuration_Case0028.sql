-- @testpoint: opengauss关键字configuration(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists configuration_test;
create table configuration_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists configuration;
create synonym configuration for configuration_test;
insert into configuration values (1,'ada'),(2, 'bob');
update configuration set configuration.name='cici' where configuration.id=2;
select * from configuration;
drop synonym if exists configuration;
--关键字带双引号-成功
drop synonym if exists "configuration";
create synonym "configuration" for configuration_test;
drop synonym if exists "configuration";

--关键字带单引号-合理报错
drop synonym if exists 'configuration';
create synonym 'configuration' for configuration_test;
insert into 'configuration' values (1,'ada'),(2, 'bob');
update 'configuration' set 'configuration'.name='cici' where 'configuration'.id=2;
select * from 'configuration';

--关键字带反引号-合理报错
drop synonym if exists `configuration`;
create synonym `configuration` for configuration_test;
insert into `configuration` values (1,'ada'),(2, 'bob');
update `configuration` set `configuration`.name='cici' where `configuration`.id=2;
select * from `configuration`;
drop table if exists configuration_test;