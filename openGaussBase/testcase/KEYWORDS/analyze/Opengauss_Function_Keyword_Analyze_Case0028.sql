-- @testpoint: opengauss关键字Analyze(保留)，作为同义词对象名,部分测试点合理报错

--前置条件
drop table if exists Analyze_test;
create table Analyze_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists Analyze;
create synonym Analyze for Analyze_test;


--关键字带双引号-成功
drop synonym if exists "Analyze";
create synonym "Analyze" for Analyze_test;
insert into "Analyze" values (1,'ada'),(2, 'bob');
update "Analyze" set "Analyze".name='cici' where "Analyze".id=2;
select * from "Analyze";

--清理环境
drop synonym "Analyze";
drop table if exists Analyze_test;
--关键字带单引号-合理报错
drop synonym if exists 'Analyze';
create synonym 'Analyze' for Analyze_test;
insert into 'Analyze' values (1,'ada'),(2, 'bob');
update 'Analyze' set 'Analyze'.name='cici' where 'Analyze'.id=2;
select * from 'Analyze';

--关键字带反引号-合理报错
drop synonym if exists `Analyze`;
create synonym `Analyze` for Analyze_test;
insert into `Analyze` values (1,'ada'),(2, 'bob');
update `Analyze` set `Analyze`.name='cici' where `Analyze`.id=2;
select * from `Analyze`;