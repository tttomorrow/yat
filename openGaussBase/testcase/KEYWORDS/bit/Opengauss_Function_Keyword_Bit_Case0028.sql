-- @testpoint: opengauss关键字bit(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists bit_test;
create table bit_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists bit;
create synonym bit for bit_test;
insert into bit values (1,'ada'),(2, 'bob');
update bit set bit.name='cici' where bit.id=2;
select * from bit;

--清理环境
drop synonym if exists bit;

--关键字带双引号-成功
drop synonym if exists "bit";
create synonym "bit" for bit_test;
insert into "bit" values (1,'ada'),(2, 'bob');
update "bit" set "bit".name='cici' where "bit".id=2;
select * from "bit";

--清理环境
drop synonym if exists "bit";

--关键字带单引号-合理报错
drop synonym if exists 'bit';

--关键字带反引号-合理报错
drop synonym if exists `bit`;
drop table if exists bit_test;