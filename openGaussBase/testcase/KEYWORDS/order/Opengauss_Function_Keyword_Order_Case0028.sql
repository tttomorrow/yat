-- @testpoint: opengauss关键字order(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists order_test;
create table order_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists order;
create synonym order for order_test;


--关键字带双引号-成功
drop synonym if exists "order";
create synonym "order" for order_test;
insert into "order" values (1,'ada'),(2, 'bob');
update "order" set "order".name='cici' where "order".id=2;
select * from "order";

--清理环境
drop synonym "order";

--关键字带单引号-合理报错
drop synonym if exists 'order';
create synonym 'order' for order_test;
insert into 'order' values (1,'ada'),(2, 'bob');
update 'order' set 'order'.name='cici' where 'order'.id=2;
select * from 'order';

--关键字带反引号-合理报错
drop synonym if exists `order`;
create synonym `order` for order_test;
insert into `order` values (1,'ada'),(2, 'bob');
update `order` set `order`.name='cici' where `order`.id=2;
select * from `order`;
--清理环境
drop table if exists order_test cascade;