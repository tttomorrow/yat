-- @testpoint: opengauss关键字As(保留)，作为同义词对象名，部分测试点合理报错

--前置条件
drop table if exists As_test;
create table As_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists As;
create synonym As for As_test;


--关键字带双引号-成功
drop synonym if exists "As";
create synonym "As" for As_test;
insert into "As" values (1,'ada'),(2, 'bob');
update "As" set "As".name='cici' where "As".id=2;
select * from "As";

--清理环境
drop synonym "As";
drop table if exists As_test;
--关键字带单引号-合理报错
drop synonym if exists 'As';
create synonym 'As' for As_test;
insert into 'As' values (1,'ada'),(2, 'bob');
update 'As' set 'As'.name='cici' where 'As'.id=2;
select * from 'As';

--关键字带反引号-合理报错
drop synonym if exists `As`;
create synonym `As` for As_test;
insert into `As` values (1,'ada'),(2, 'bob');
update `As` set `As`.name='cici' where `As`.id=2;
select * from `As`;