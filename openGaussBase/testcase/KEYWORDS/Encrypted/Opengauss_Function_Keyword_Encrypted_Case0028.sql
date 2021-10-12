-- @testpoint: opengauss关键字encrypted(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists encrypted_test;
create table encrypted_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists encrypted;
create synonym encrypted for encrypted_test;
insert into encrypted values (1,'ada'),(2, 'bob');
update encrypted set encrypted.name='cici' where encrypted.id=2;
select * from encrypted;
drop synonym if exists encrypted;

--关键字带双引号-成功
drop synonym if exists "encrypted";
create synonym "encrypted" for encrypted_test;
drop synonym if exists "encrypted";

--关键字带单引号-合理报错
drop synonym if exists 'encrypted';
create synonym 'encrypted' for encrypted_test;
insert into 'encrypted' values (1,'ada'),(2, 'bob');
update 'encrypted' set 'encrypted'.name='cici' where 'encrypted'.id=2;
select * from 'encrypted';

--关键字带反引号-合理报错
drop synonym if exists `encrypted`;
create synonym `encrypted` for encrypted_test;
insert into `encrypted` values (1,'ada'),(2, 'bob');
update `encrypted` set `encrypted`.name='cici' where `encrypted`.id=2;
select * from `encrypted`;
drop table if exists encrypted_test;