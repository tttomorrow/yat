-- @testpoint: opengauss关键字add(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists add_test;
create table add_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists add;
create synonym add for add_test;
insert into add values (1,'ada'),(2, 'bob');
update add set add.name='cici' where add.id=2;
select * from add;

--清理环境
drop synonym if exists add;

--关键字带双引号-成功
drop synonym if exists "add";
create synonym "add" for add_test;
insert into "add" values (1,'ada'),(2, 'bob');
update "add" set "add".name='cici' where "add".id=2;
select * from "add";

--清理环境
drop synonym if exists "add";

--关键字带单引号-合理报错
drop synonym if exists 'add';

--关键字带反引号-合理报错
drop synonym if exists `add`;
drop table if exists add_test;