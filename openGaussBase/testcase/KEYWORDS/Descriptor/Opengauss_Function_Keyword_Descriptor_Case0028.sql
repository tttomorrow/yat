-- @testpoint: opengauss关键字descriptor(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists descriptor_test;
create table descriptor_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists descriptor;
create synonym descriptor for descriptor_test;
insert into descriptor values (1,'ada'),(2, 'bob');
update descriptor set descriptor.name='cici' where descriptor.id=2;
select * from descriptor;
drop synonym descriptor;

--关键字带双引号-成功
drop synonym if exists "descriptor";
create synonym "descriptor" for descriptor_test;
drop synonym "descriptor";


--关键字带单引号-合理报错
drop synonym if exists 'descriptor';
create synonym 'descriptor' for descriptor_test;
insert into 'descriptor' values (1,'ada'),(2, 'bob');
update 'descriptor' set 'descriptor'.name='cici' where 'descriptor'.id=2;
select * from 'descriptor';

--关键字带反引号-合理报错
drop synonym if exists `descriptor`;
create synonym `descriptor` for descriptor_test;
insert into `descriptor` values (1,'ada'),(2, 'bob');
update `descriptor` set `descriptor`.name='cici' where `descriptor`.id=2;
select * from `descriptor`;
drop table if exists descriptor_test;