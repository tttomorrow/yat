-- @testpoint: opengauss关键字exchange(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists exchange_test;
create table exchange_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists exchange;
create synonym exchange for exchange_test;
insert into exchange values (1,'ada'),(2, 'bob');
update exchange set exchange.name='cici' where exchange.id=2;
select * from exchange;
drop synonym if exists exchange;

--关键字带双引号-成功
drop synonym if exists "exchange";
create synonym "exchange" for exchange_test;
drop synonym if exists "exchange";

--关键字带单引号-合理报错
drop synonym if exists 'exchange';
create synonym 'exchange' for exchange_test;
insert into 'exchange' values (1,'ada'),(2, 'bob');
update 'exchange' set 'exchange'.name='cici' where 'exchange'.id=2;
select * from 'exchange';

--关键字带反引号-合理报错
drop synonym if exists `exchange`;
create synonym `exchange` for exchange_test;
insert into `exchange` values (1,'ada'),(2, 'bob');
update `exchange` set `exchange`.name='cici' where `exchange`.id=2;
select * from `exchange`;
drop table if exists exchange_test;