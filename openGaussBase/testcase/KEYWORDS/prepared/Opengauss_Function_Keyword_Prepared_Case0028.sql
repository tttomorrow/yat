-- @testpoint: opengauss关键字prepared(非保留)，作为同义词对象名,合理报错


--前置条件
drop table if exists prepared_test;
create table prepared_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists prepared;
create synonym prepared for prepared_test;
insert into prepared values (1,'ada'),(2, 'bob');
update prepared set prepared.name='cici' where prepared.id=2;
select * from prepared;

--关键字带双引号-成功
drop synonym if exists "prepared";
create synonym "prepared" for prepared_test;
insert into "prepared" values (1,'ada'),(2, 'bob');
update "prepared" set "prepared".name='cici' where "prepared".id=2;
select * from "prepared";

--关键字带单引号-合理报错
drop synonym if exists 'prepared';
create synonym 'prepared' for prepared_test;

--关键字带反引号-合理报错
drop synonym if exists `prepared`;
create synonym `prepared` for prepared_test;

--清理环境
drop table if exists prepared_test;
drop synonym if exists prepared;
drop synonym if exists "prepared";