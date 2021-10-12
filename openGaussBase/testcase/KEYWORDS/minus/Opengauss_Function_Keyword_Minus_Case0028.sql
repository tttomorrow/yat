-- @testpoint: opengauss关键字minus(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists minus_test;
create table minus_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists minus;
create synonym minus for minus_test;


--关键字带双引号-成功
drop synonym if exists "minus";
create synonym "minus" for minus_test;
insert into "minus" values (1,'ada'),(2, 'bob');
update "minus" set "minus".name='cici' where "minus".id=2;
select * from "minus";

--清理环境
drop synonym "minus";

--关键字带单引号-合理报错
drop synonym if exists 'minus';
create synonym 'minus' for minus_test;
insert into 'minus' values (1,'ada'),(2, 'bob');
update 'minus' set 'minus'.name='cici' where 'minus'.id=2;
select * from 'minus';

--关键字带反引号-合理报错
drop synonym if exists `minus`;
create synonym `minus` for minus_test;
insert into `minus` values (1,'ada'),(2, 'bob');
update `minus` set `minus`.name='cici' where `minus`.id=2;
select * from `minus`;
--清理环境
drop table if exists minus_test;