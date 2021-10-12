-- @testpoint: opengauss关键字dec(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists dec_test;
create table dec_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists dec;
create synonym dec for dec_test;
insert into dec values (1,'ada'),(2, 'bob');
update dec set dec.name='cici' where dec.id=2;
select * from dec;
drop synonym if exists dec;

--关键字带双引号-成功
drop synonym if exists "dec";
create synonym "dec" for dec_test;
drop synonym if exists "dec";

--关键字带单引号-合理报错
drop synonym if exists 'dec';
create synonym 'dec' for dec_test;
insert into 'dec' values (1,'ada'),(2, 'bob');
update 'dec' set 'dec'.name='cici' where 'dec'.id=2;
select * from 'dec';

--关键字带反引号-合理报错
drop synonym if exists `dec`;
create synonym `dec` for dec_test;
insert into `dec` values (1,'ada'),(2, 'bob');
update `dec` set `dec`.name='cici' where `dec`.id=2;
select * from `dec`;
drop table if exists dec_test;