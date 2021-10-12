-- @testpoint: opengauss关键字connect(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists connect_test;
create table connect_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists connect;
create synonym connect for connect_test;
insert into connect values (1,'ada'),(2, 'bob');
update connect set connect.name='cici' where connect.id=2;
select * from connect;
drop synonym if exists connect;
--关键字带双引号-成功
drop synonym if exists "connect";
create synonym "connect" for connect_test;
drop synonym if exists "connect";

--关键字带单引号-合理报错
drop synonym if exists 'connect';
create synonym 'connect' for connect_test;
insert into 'connect' values (1,'ada'),(2, 'bob');
update 'connect' set 'connect'.name='cici' where 'connect'.id=2;
select * from 'connect';

--关键字带反引号-合理报错
drop synonym if exists `connect`;
create synonym `connect` for connect_test;
insert into `connect` values (1,'ada'),(2, 'bob');
update `connect` set `connect`.name='cici' where `connect`.id=2;
select * from `connect`;
drop table if exists connect_test;