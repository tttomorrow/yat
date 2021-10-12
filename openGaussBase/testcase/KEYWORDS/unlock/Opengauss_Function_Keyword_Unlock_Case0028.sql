-- @testpoint: opengauss关键字unlock(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists unlock;
create synonym unlock for explain_test;
insert into unlock values (1,'ada'),(2, 'bob');
update unlock set unlock.name='cici' where unlock.id=2;
select * from unlock;
drop synonym if exists unlock;

--关键字带双引号-成功
drop synonym if exists "unlock";
create synonym "unlock" for explain_test;
drop synonym if exists "unlock";

--关键字带单引号-合理报错
drop synonym if exists 'unlock';
create synonym 'unlock' for explain_test;
insert into 'unlock' values (1,'ada'),(2, 'bob');
update 'unlock' set 'unlock'.name='cici' where 'unlock'.id=2;
select * from 'unlock';

--关键字带反引号-合理报错
drop synonym if exists `unlock`;
create synonym `unlock` for explain_test;
insert into `unlock` values (1,'ada'),(2, 'bob');
update `unlock` set `unlock`.name='cici' where `unlock`.id=2;
select * from `unlock`;

--清理环境
drop table if exists explain_test;