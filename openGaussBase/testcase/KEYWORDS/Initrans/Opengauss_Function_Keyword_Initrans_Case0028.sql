-- @testpoint: opengauss关键字Initrans(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists explain_test;
create table explain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists Initrans;
create synonym Initrans for explain_test;
insert into Initrans values (1,'ada'),(2, 'bob');
update Initrans set Initrans.name='cici' where Initrans.id=2;
select * from Initrans;

--关键字带双引号-成功
drop synonym if exists "Initrans";
create synonym "Initrans" for explain_test;


--关键字带单引号-合理报错
drop synonym if exists 'Initrans';
create synonym 'Initrans' for explain_test;
insert into 'Initrans' values (1,'ada'),(2, 'bob');
update 'Initrans' set 'Initrans'.name='cici' where 'Initrans'.id=2;
select * from 'Initrans';

--关键字带反引号-合理报错
drop synonym if exists `Initrans`;
create synonym `Initrans` for explain_test;
insert into `Initrans` values (1,'ada'),(2, 'bob');
update `Initrans` set `Initrans`.name='cici' where `Initrans`.id=2;
select * from `Initrans`;
--清理环境
drop synonym if exists initrans;
drop synonym if exists "Initrans";
drop table if exists explain_test;