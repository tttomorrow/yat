-- @testpoint: opengauss关键字unique(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists unique_test;
create table unique_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists unique;
create synonym unique for unique_test;


--关键字带双引号-成功
drop synonym if exists "unique";
create synonym "unique" for unique_test;
insert into "unique" values (1,'ada'),(2, 'bob');
update "unique" set "unique".name='cici' where "unique".id=2;
select * from "unique";
drop synonym "unique";
--关键字带单引号-合理报错
drop synonym if exists 'unique';
create synonym 'unique' for unique_test;
insert into 'unique' values (1,'ada'),(2, 'bob');
update 'unique' set 'unique'.name='cici' where 'unique'.id=2;
select * from 'unique';

--关键字带反引号-合理报错
drop synonym if exists `unique`;
create synonym `unique` for unique_test;
insert into `unique` values (1,'ada'),(2, 'bob');
update `unique` set `unique`.name='cici' where `unique`.id=2;
select * from `unique`;

--清理环境
drop table if exists unique_test;