-- @testpoint: opengauss关键字Array(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists Array_test;
create table Array_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists Array;
create synonym Array for Array_test;


--关键字带双引号-成功
drop synonym if exists "Array";
create synonym "Array" for Array_test;
insert into "Array" values (1,'ada'),(2, 'bob');
update "Array" set "Array".name='cici' where "Array".id=2;
select * from "Array";

--清理环境
drop synonym "Array";

--关键字带单引号-合理报错
drop synonym if exists 'Array';
create synonym 'Array' for Array_test;
insert into 'Array' values (1,'ada'),(2, 'bob');
update 'Array' set 'Array'.name='cici' where 'Array'.id=2;
select * from 'Array';

--关键字带反引号-合理报错
drop synonym if exists `Array`;
create synonym `Array` for Array_test;
insert into `Array` values (1,'ada'),(2, 'bob');
update `Array` set `Array`.name='cici' where `Array`.id=2;
select * from `Array`;
drop table if exists Array_test;