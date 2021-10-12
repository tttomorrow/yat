-- @testpoint: opengauss关键字float(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists float_test;
create table float_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists float;
create synonym float for float_test;
insert into float values (1,'ada'),(2, 'bob');
update float set float.name='cici' where float.id=2;
select * from float;
drop synonym if exists float;

--关键字带双引号-成功
drop synonym if exists "float";
create synonym "float" for float_test;
drop synonym if exists "float";

--关键字带单引号-合理报错
drop synonym if exists 'float';
create synonym 'float' for float_test;
insert into 'float' values (1,'ada'),(2, 'bob');
update 'float' set 'float'.name='cici' where 'float'.id=2;
select * from 'float';

--关键字带反引号-合理报错
drop synonym if exists `float`;
create synonym `float` for float_test;
insert into `float` values (1,'ada'),(2, 'bob');
update `float` set `float`.name='cici' where `float`.id=2;
select * from `float`;
drop table if exists float_test;