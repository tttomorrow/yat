-- @testpoint: opengauss关键字connection(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists connection_test;
create table connection_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists connection;
create synonym connection for connection_test;
insert into connection values (1,'ada'),(2, 'bob');
update connection set connection.name='cici' where connection.id=2;
select * from connection;
drop synonym if exists connection;
--关键字带双引号-成功
drop synonym if exists "connection";
create synonym "connection" for connection_test;
drop synonym if exists "connection";

--关键字带单引号-合理报错
drop synonym if exists 'connection';
create synonym 'connection' for connection_test;
insert into 'connection' values (1,'ada'),(2, 'bob');
update 'connection' set 'connection'.name='cici' where 'connection'.id=2;
select * from 'connection';

--关键字带反引号-合理报错
drop synonym if exists `connection`;
create synonym `connection` for connection_test;
insert into `connection` values (1,'ada'),(2, 'bob');
update `connection` set `connection`.name='cici' where `connection`.id=2;
select * from `connection`;
drop table if exists connection_test;