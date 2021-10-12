-- @testpoint: opengauss关键字data(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists data_test;
create table data_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists data;
create synonym data for data_test;
insert into data values (1,'ada'),(2, 'bob');
update data set data.name='cici' where data.id=2;
select * from data;
drop synonym if exists data;

--关键字带双引号-成功
drop synonym if exists "data";
create synonym "data" for data_test;
drop synonym if exists "data";

--关键字带单引号-合理报错
drop synonym if exists 'data';
create synonym 'data' for data_test;
insert into 'data' values (1,'ada'),(2, 'bob');
update 'data' set 'data'.name='cici' where 'data'.id=2;
select * from 'data';

--关键字带反引号-合理报错
drop synonym if exists `data`;
create synonym `data` for data_test;
insert into `data` values (1,'ada'),(2, 'bob');
update `data` set `data`.name='cici' where `data`.id=2;
select * from `data`;
drop table if exists data_test;