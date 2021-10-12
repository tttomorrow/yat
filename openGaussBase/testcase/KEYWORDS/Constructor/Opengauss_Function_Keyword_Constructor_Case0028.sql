-- @testpoint: opengauss关键字constructor(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists constructor_test;
create table constructor_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists constructor;
create synonym constructor for constructor_test;
insert into constructor values (1,'ada'),(2, 'bob');
update constructor set constructor.name='cici' where constructor.id=2;
select * from constructor;

--关键字带双引号-成功
drop synonym if exists "constructor";
create synonym "constructor" for constructor_test;


--关键字带单引号-合理报错
drop synonym if exists 'constructor';
create synonym 'constructor' for constructor_test;
insert into 'constructor' values (1,'ada'),(2, 'bob');
update 'constructor' set 'constructor'.name='cici' where 'constructor'.id=2;
select * from 'constructor';

--关键字带反引号-合理报错
drop synonym if exists `constructor`;
create synonym `constructor` for constructor_test;
insert into `constructor` values (1,'ada'),(2, 'bob');
update `constructor` set `constructor`.name='cici' where `constructor`.id=2;
select * from `constructor`;

--清理环境
drop table if exists constructor_test;
drop synonym if exists constructor;
drop synonym if exists "constructor";