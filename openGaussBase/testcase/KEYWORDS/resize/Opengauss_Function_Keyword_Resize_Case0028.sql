-- @testpoint: opengauss关键字resize(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists resize_test;
create table resize_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists resize;
create synonym resize for resize_test;
insert into resize values (1,'ada'),(2, 'bob');
update resize set resize.name='cici' where resize.id=2;
select * from resize;
drop synonym if exists resize;

--关键字带双引号-成功
drop synonym if exists "resize";
create synonym "resize" for resize_test;
insert into "resize" values (1,'ada'),(2, 'bob');
update "resize" set "resize".name='cici' where "resize".id=2;
select * from "resize";
drop synonym if exists "resize";

--关键字带单引号-合理报错
drop synonym if exists 'resize';

--关键字带反引号-合理报错
drop synonym if exists `resize`;
drop table if exists resize_test;