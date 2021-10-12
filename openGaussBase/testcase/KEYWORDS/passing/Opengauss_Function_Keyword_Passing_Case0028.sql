-- @testpoint: opengauss关键字passing(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists passing;
create synonym passing for explain_test;
insert into passing values (1,'ada'),(2, 'bob');
update passing set passing.name='cici' where passing.id=2;
select * from passing;

--关键字带双引号-成功
drop synonym if exists "passing";
create synonym "passing" for explain_test;


--关键字带单引号-合理报错
drop synonym if exists 'passing';
create synonym 'passing' for explain_test;
insert into 'passing' values (1,'ada'),(2, 'bob');
update 'passing' set 'passing'.name='cici' where 'passing'.id=2;
select * from 'passing';

--关键字带反引号-合理报错
drop synonym if exists `passing`;
create synonym `passing` for explain_test;
insert into `passing` values (1,'ada'),(2, 'bob');
update `passing` set `passing`.name='cici' where `passing`.id=2;
select * from `passing`;
--清理环境
drop synonym if exists "passing";
drop synonym if exists passing;
drop table if exists explain_test;
