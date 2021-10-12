-- @testpoint: opengauss关键字Isolation(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists Isolation;
create synonym Isolation for explain_test;
insert into Isolation values (1,'ada'),(2, 'bob');
update Isolation set Isolation.name='cici' where Isolation.id=2;
select * from Isolation;

--关键字带双引号-成功
drop synonym if exists "Isolation";
create synonym "Isolation" for explain_test;


--关键字带单引号-合理报错
drop synonym if exists 'Isolation';
create synonym 'Isolation' for explain_test;
insert into 'Isolation' values (1,'ada'),(2, 'bob');
update 'Isolation' set 'Isolation'.name='cici' where 'Isolation'.id=2;
select * from 'Isolation';

--关键字带反引号-合理报错
drop synonym if exists `Isolation`;
create synonym `Isolation` for explain_test;
insert into `Isolation` values (1,'ada'),(2, 'bob');
update `Isolation` set `Isolation`.name='cici' where `Isolation`.id=2;
select * from `Isolation`;
--清理环境
drop synonym if exists isolation;
drop synonym if exists "Isolation";
drop table if exists explain_test;