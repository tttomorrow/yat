-- @testpoint: opengauss关键字Granted(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists Granted;
create synonym Granted for explain_test;
insert into Granted values (1,'ada'),(2, 'bob');
update Granted set Granted.name='cici' where Granted.id=2;
select * from Granted;
drop synonym if exists Granted;

--关键字带双引号-成功
drop synonym if exists "Granted";
create synonym "Granted" for explain_test;
drop synonym if exists "Granted";

--关键字带单引号-合理报错
drop synonym if exists 'Granted';
create synonym 'Granted' for explain_test;
insert into 'Granted' values (1,'ada'),(2, 'bob');
update 'Granted' set 'Granted'.name='cici' where 'Granted'.id=2;
select * from 'Granted';

--关键字带反引号-合理报错
drop synonym if exists `Granted`;
create synonym `Granted` for explain_test;
insert into `Granted` values (1,'ada'),(2, 'bob');
update `Granted` set `Granted`.name='cici' where `Granted`.id=2;
select * from `Granted`;

--清理环境
drop table if exists grant_test;