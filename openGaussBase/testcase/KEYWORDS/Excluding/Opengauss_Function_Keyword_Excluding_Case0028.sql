-- @testpoint: opengauss关键字excluding(非保留)，作为同义词对象名，部分测试点合理报错

--前置条件
drop table if exists excluding_test;
create table excluding_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists excluding;
create synonym excluding for excluding_test;
insert into excluding values (1,'ada'),(2, 'bob');
update excluding set excluding.name='cici' where excluding.id=2;
select * from excluding;
drop synonym if exists excluding;

--关键字带双引号-成功
drop synonym if exists "excluding";
create synonym "excluding" for excluding_test;
drop synonym if exists "excluding";

--关键字带单引号-合理报错
drop synonym if exists 'excluding';
create synonym 'excluding' for excluding_test;
insert into 'excluding' values (1,'ada'),(2, 'bob');
update 'excluding' set 'excluding'.name='cici' where 'excluding'.id=2;
select * from 'excluding';

--关键字带反引号-合理报错
drop synonym if exists `excluding`;
create synonym `excluding` for excluding_test;
insert into `excluding` values (1,'ada'),(2, 'bob');
update `excluding` set `excluding`.name='cici' where `excluding`.id=2;
select * from `excluding`;
drop table if exists excluding_test;