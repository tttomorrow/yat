-- @testpoint: opengauss关键字ref非保留)，作为索引名，部分测试点合理报错

--前置条件，创建一个表
drop table if exists ref_test;
create table ref_test(id int,name varchar(10));

--关键字不带引号-成功
drop index if exists ref;
create index ref on ref_test(id);
drop index ref;

--关键字带双引号-成功
drop index if exists "ref";
create index "ref" on ref_test(id);
drop index "ref";

--关键字带单引号-合理报错
drop index if exists 'ref';


--关键字带反引号-合理报错
drop index if exists `ref`;
drop table if exists ref_test;