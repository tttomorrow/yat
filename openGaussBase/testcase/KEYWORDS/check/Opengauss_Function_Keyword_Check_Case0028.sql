-- @testpoint: opengauss关键字Check(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists Check_test;
create table Check_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists Check;
create synonym Check for Check_test;


--关键字带双引号-成功
drop synonym if exists "Check";
create synonym "Check" for Check_test;
insert into "Check" values (1,'ada'),(2, 'bob');
update "Check" set "Check".name='cici' where "Check".id=2;
select * from "Check";

--清理环境
drop synonym "Check";

--关键字带单引号-合理报错
drop synonym if exists 'Check';
create synonym 'Check' for Check_test;
insert into 'Check' values (1,'ada'),(2, 'bob');
update 'Check' set 'Check'.name='cici' where 'Check'.id=2;
select * from 'Check';

--关键字带反引号-合理报错
drop synonym if exists `Check`;
create synonym `Check` for Check_test;
insert into `Check` values (1,'ada'),(2, 'bob');
update `Check` set `Check`.name='cici' where `Check`.id=2;
select * from `Check`;
drop table if exists Check_test;