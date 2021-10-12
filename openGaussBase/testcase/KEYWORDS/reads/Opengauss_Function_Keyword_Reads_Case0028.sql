-- @testpoint: opengauss关键字reads(非保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists reads_test;
create table reads_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists reads;
create synonym reads for reads_test;
insert into reads values (1,'ada'),(2, 'bob');
update reads set reads.name='cici' where reads.id=2;
select * from reads;
drop synonym if exists reads;

--关键字带双引号-成功
drop synonym if exists "reads";
create synonym "reads" for reads_test;
insert into "reads" values (1,'ada'),(2, 'bob');
update "reads" set "reads".name='cici' where "reads".id=2;
select * from "reads";
drop synonym if exists "reads";

--关键字带单引号-合理报错
drop synonym if exists 'reads';

--关键字带反引号-合理报错
drop synonym if exists `reads`;
--清理环境
drop table if exists reads_test;