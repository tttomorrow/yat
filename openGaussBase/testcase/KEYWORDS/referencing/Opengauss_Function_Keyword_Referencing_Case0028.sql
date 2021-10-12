-- @testpoint: opengauss关键字referencing(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists referencing_test;
create table referencing_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists referencing;
create synonym referencing for referencing_test;
insert into referencing values (1,'ada'),(2, 'bob');
update referencing set referencing.name='cici' where referencing.id=2;
select * from referencing;
drop synonym if exists referencing;

--关键字带双引号-成功
drop synonym if exists "referencing";
create synonym "referencing" for referencing_test;
insert into "referencing" values (1,'ada'),(2, 'bob');
update "referencing" set "referencing".name='cici' where "referencing".id=2;
select * from "referencing";
drop synonym if exists "referencing";

--关键字带单引号-合理报错
drop synonym if exists 'referencing';

--关键字带反引号-合理报错
drop synonym if exists `referencing`;
drop table if exists referencing_test;