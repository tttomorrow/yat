-- @testpoint: opengauss关键字national(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists national;
create synonym national for explain_test;
insert into national values (1,'ada'),(2, 'bob');
update national set national.name='cici' where national.id=2;
select * from national;

--关键字带双引号-成功
drop synonym if exists "national";
create synonym "national" for explain_test;


--关键字带单引号-合理报错
drop synonym if exists 'national';
create synonym 'national' for explain_test;
insert into 'national' values (1,'ada'),(2, 'bob');
update 'national' set 'national'.name='cici' where 'national'.id=2;
select * from 'national';

--关键字带反引号-合理报错
drop synonym if exists `national`;
create synonym `national` for explain_test;
insert into `national` values (1,'ada'),(2, 'bob');
update `national` set `national`.name='cici' where `national`.id=2;
select * from `national`;
--清理环境
drop synonym if exists "national";
drop synonym if exists national;
drop table if exists explain_test;