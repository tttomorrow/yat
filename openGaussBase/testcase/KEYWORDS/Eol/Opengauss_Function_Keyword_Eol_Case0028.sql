-- @testpoint: opengauss关键字eol(非保留)，作为同义词对象名，部分测试点合理报错

--前置条件
drop table if exists eol_test;
create table eol_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists eol;
create synonym eol for eol_test;
insert into eol values (1,'ada'),(2, 'bob');
update eol set eol.name='cici' where eol.id=2;
select * from eol;
drop synonym if exists eol;

--关键字带双引号-成功
drop synonym if exists "eol";
create synonym "eol" for eol_test;
drop synonym if exists "eol";

--关键字带单引号-合理报错
drop synonym if exists 'eol';
create synonym 'eol' for eol_test;
insert into 'eol' values (1,'ada'),(2, 'bob');
update 'eol' set 'eol'.name='cici' where 'eol'.id=2;
select * from 'eol';

--关键字带反引号-合理报错
drop synonym if exists `eol`;
create synonym `eol` for eol_test;
insert into `eol` values (1,'ada'),(2, 'bob');
update `eol` set `eol`.name='cici' where `eol`.id=2;
select * from `eol`;
drop table if exists eol_test;