-- @testpoint: opengauss关键字extract(非保留)，作为同义词对象名，部分测试点合理报错

--前置条件
drop table if exists extract_test;
create table extract_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists extract;
create synonym extract for extract_test;
insert into extract values (1,'ada'),(2, 'bob');
update extract set extract.name='cici' where extract.id=2;
select * from extract;
drop synonym if exists extract;

--关键字带双引号-成功
drop synonym if exists "extract";
create synonym "extract" for extract_test;
drop synonym if exists "extract";

--关键字带单引号-合理报错
drop synonym if exists 'extract';
create synonym 'extract' for extract_test;
insert into 'extract' values (1,'ada'),(2, 'bob');
update 'extract' set 'extract'.name='cici' where 'extract'.id=2;
select * from 'extract';

--关键字带反引号-合理报错
drop synonym if exists `extract`;
create synonym `extract` for extract_test;
insert into `extract` values (1,'ada'),(2, 'bob');
update `extract` set `extract`.name='cici' where `extract`.id=2;
select * from `extract`;
drop table if exists extract_test;