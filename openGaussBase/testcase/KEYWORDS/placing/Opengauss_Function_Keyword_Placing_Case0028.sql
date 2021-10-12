-- @testpoint: opengauss关键字placing(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists placing_test;
create table placing_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists placing;
create synonym placing for placing_test;


--关键字带双引号-成功
drop synonym if exists "placing";
create synonym "placing" for placing_test;
insert into "placing" values (1,'ada'),(2, 'bob');
update "placing" set "placing".name='cici' where "placing".id=2;
select * from "placing";

--清理环境
drop synonym "placing";

--关键字带单引号-合理报错
drop synonym if exists 'placing';
create synonym 'placing' for placing_test;
insert into 'placing' values (1,'ada'),(2, 'bob');
update 'placing' set 'placing'.name='cici' where 'placing'.id=2;
select * from 'placing';

--关键字带反引号-合理报错
drop synonym if exists `placing`;
create synonym `placing` for placing_test;
insert into `placing` values (1,'ada'),(2, 'bob');
update `placing` set `placing`.name='cici' where `placing`.id=2;
select * from `placing`;
--清理环境
drop table if exists placing_test cascade;