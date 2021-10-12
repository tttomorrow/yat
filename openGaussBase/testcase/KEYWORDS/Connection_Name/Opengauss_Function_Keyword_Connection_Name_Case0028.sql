-- @testpoint: opengauss关键字connection_name(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists connection_name_test;
create table connection_name_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists connection_name;
create synonym connection_name for connection_name_test;
insert into connection_name values (1,'ada'),(2, 'bob');
update connection_name set connection_name.name='cici' where connection_name.id=2;
select * from connection_name;
drop synonym if exists connection_name;
--关键字带双引号-成功
drop synonym if exists "connection_name";
create synonym "connection_name" for connection_name_test;
drop synonym if exists "connection_name";

--关键字带单引号-合理报错
drop synonym if exists 'connection_name';
create synonym 'connection_name' for connection_name_test;
insert into 'connection_name' values (1,'ada'),(2, 'bob');
update 'connection_name' set 'connection_name'.name='cici' where 'connection_name'.id=2;
select * from 'connection_name';

--关键字带反引号-合理报错
drop synonym if exists `connection_name`;
create synonym `connection_name` for connection_name_test;
insert into `connection_name` values (1,'ada'),(2, 'bob');
update `connection_name` set `connection_name`.name='cici' where `connection_name`.id=2;
select * from `connection_name`;
drop table if exists connection_name_test;