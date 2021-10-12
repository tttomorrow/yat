-- @testpoint: opengauss关键字real(非保留)，作为同义词对象名,部分测试点合理报错

--前置条件
drop table if exists real_test;
create table real_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists real;
create synonym real for real_test;
insert into real values (1,'ada'),(2, 'bob');
update real set real.name='cici' where real.id=2;
select * from real;
drop synonym if exists real;

--关键字带双引号-成功
drop synonym if exists "real";
create synonym "real" for real_test;
insert into "real" values (1,'ada'),(2, 'bob');
update "real" set "real".name='cici' where "real".id=2;
select * from "real";
drop synonym if exists "real";

--关键字带单引号-合理报错
drop synonym if exists 'real';

--关键字带反引号-合理报错
drop synonym if exists `real`;
--清理环境
drop table if exists real_test;
