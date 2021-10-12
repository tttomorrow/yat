-- @testpoint: opengauss关键字escaping(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists escaping_test;
create table escaping_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists escaping;
create synonym escaping for escaping_test;
insert into escaping values (1,'ada'),(2, 'bob');
update escaping set escaping.name='cici' where escaping.id=2;
select * from escaping;
drop synonym if exists escaping;

--关键字带双引号-成功
drop synonym if exists "escaping";
create synonym "escaping" for escaping_test;
drop synonym if exists "escaping";

--关键字带单引号-合理报错
drop synonym if exists 'escaping';
create synonym 'escaping' for escaping_test;
insert into 'escaping' values (1,'ada'),(2, 'bob');
update 'escaping' set 'escaping'.name='cici' where 'escaping'.id=2;
select * from 'escaping';

--关键字带反引号-合理报错
drop synonym if exists `escaping`;
create synonym `escaping` for escaping_test;
insert into `escaping` values (1,'ada'),(2, 'bob');
update `escaping` set `escaping`.name='cici' where `escaping`.id=2;
select * from `escaping`;
drop table if exists escaping_test;