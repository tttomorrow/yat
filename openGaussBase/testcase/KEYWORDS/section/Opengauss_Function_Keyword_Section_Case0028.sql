-- @testpoint: opengauss关键字section(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists section;
create synonym section for explain_test;
insert into section values (1,'ada'),(2, 'bob');
update section set section.name='cici' where section.id=2;
select * from section;
drop synonym if exists section;

--关键字带双引号-成功
drop synonym if exists "section";
create synonym "section" for explain_test;
drop synonym if exists "section";

--关键字带单引号-合理报错
drop synonym if exists 'section';
create synonym 'section' for explain_test;
insert into 'section' values (1,'ada'),(2, 'bob');
update 'section' set 'section'.name='cici' where 'section'.id=2;
select * from 'section';

--关键字带反引号-合理报错
drop synonym if exists `section`;
create synonym `section` for explain_test;
insert into `section` values (1,'ada'),(2, 'bob');
update `section` set `section`.name='cici' where `section`.id=2;
select * from `section`;
drop table if exists explain_test;