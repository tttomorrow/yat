-- @testpoint: opengauss关键字distribution(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists distribution_test;
create table distribution_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists distribution;
create synonym distribution for distribution_test;
insert into distribution values (1,'ada'),(2, 'bob');
update distribution set distribution.name='cici' where distribution.id=2;
select * from distribution;
drop synonym if exists distribution;

--关键字带双引号-成功
drop synonym if exists "distribution";
create synonym "distribution" for distribution_test;
drop synonym if exists "distribution";

--关键字带单引号-合理报错
drop synonym if exists 'distribution';
create synonym 'distribution' for distribution_test;
insert into 'distribution' values (1,'ada'),(2, 'bob');
update 'distribution' set 'distribution'.name='cici' where 'distribution'.id=2;
select * from 'distribution';

--关键字带反引号-合理报错
drop synonym if exists `distribution`;
create synonym `distribution` for distribution_test;
insert into `distribution` values (1,'ada'),(2, 'bob');
update `distribution` set `distribution`.name='cici' where `distribution`.id=2;
select * from `distribution`;
drop table if exists distribution_test;