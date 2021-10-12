-- @testpoint: opengauss关键字deref(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists deref_test;
create table deref_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists deref;
create synonym deref for deref_test;
insert into deref values (1,'ada'),(2, 'bob');
update deref set deref.name='cici' where deref.id=2;
select * from deref;
drop synonym if exists deref;

--关键字带双引号-成功
drop synonym if exists "deref";
create synonym "deref" for deref_test;
drop synonym if exists "deref";

--关键字带单引号-合理报错
drop synonym if exists 'deref';
create synonym 'deref' for deref_test;
insert into 'deref' values (1,'ada'),(2, 'bob');
update 'deref' set 'deref'.name='cici' where 'deref'.id=2;
select * from 'deref';

--关键字带反引号-合理报错
drop synonym if exists `deref`;
create synonym `deref` for deref_test;
insert into `deref` values (1,'ada'),(2, 'bob');
update `deref` set `deref`.name='cici' where `deref`.id=2;
select * from `deref`;
drop table if exists deref_test;