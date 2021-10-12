-- @testpoint: opengauss关键字freeze(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists freeze_test;
create table freeze_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists freeze;
create synonym freeze for freeze_test;


--关键字带双引号-成功
drop synonym if exists "freeze";
create synonym "freeze" for freeze_test;
insert into "freeze" values (1,'ada'),(2, 'bob');
update "freeze" set "freeze".name='cici' where "freeze".id=2;
select * from "freeze";

--清理环境
drop synonym "freeze";

--关键字带单引号-合理报错
drop synonym if exists 'freeze';
create synonym 'freeze' for freeze_test;
insert into 'freeze' values (1,'ada'),(2, 'bob');
update 'freeze' set 'freeze'.name='cici' where 'freeze'.id=2;
select * from 'freeze';

--关键字带反引号-合理报错
drop synonym if exists `freeze`;
create synonym `freeze` for freeze_test;
insert into `freeze` values (1,'ada'),(2, 'bob');
update `freeze` set `freeze`.name='cici' where `freeze`.id=2;
select * from `freeze`;

--清理环境
drop table if exists freeze_test;