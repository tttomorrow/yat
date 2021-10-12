--  @testpoint:opengauss关键字cube(非保留)，作为索引名

--前置条件，创建一个表
drop table if exists cube_test;
create table cube_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists cube;
create index cube on cube_test(id);
drop index cube;

--关键字带双引号-成功
drop index if exists "cube";
create index "cube" on cube_test(id);
drop index "cube";

--关键字带单引号-合理报错
drop index if exists 'cube';
create index 'cube' on cube_test(id);

--关键字带反引号-合理报错
drop index if exists `cube`;
create index `cube` on cube_test(id);
