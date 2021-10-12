--  @testpoint:opengauss关键字procedural非保留)，作为序列名


--关键字不带引号-成功
drop sequence if exists procedural;
create sequence procedural start 100 cache 50;
drop sequence procedural;

--关键字带双引号-成功
drop sequence if exists "procedural";
create sequence "procedural" start 100 cache 50;
drop sequence "procedural";

--关键字带单引号-合理报错
drop sequence if exists 'procedural';

--关键字带反引号-合理报错
drop sequence if exists `procedural`;

