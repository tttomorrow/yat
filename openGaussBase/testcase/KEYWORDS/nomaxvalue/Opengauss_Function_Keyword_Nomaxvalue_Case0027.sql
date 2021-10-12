--  @testpoint:opengauss关键字nomaxvalue非保留)，作为序列名


--关键字不带引号-成功
drop sequence if exists nomaxvalue;
create sequence nomaxvalue start 100 cache 50;
drop sequence nomaxvalue;

--关键字带双引号-成功
drop sequence if exists "nomaxvalue";
create sequence "nomaxvalue" start 100 cache 50;
drop sequence "nomaxvalue";

--关键字带单引号-合理报错
drop sequence if exists 'nomaxvalue';
create sequence 'nomaxvalue' start 100 cache 50;

--关键字带反引号-合理报错
drop sequence if exists `nomaxvalue`;
create sequence `nomaxvalue` start 100 cache 50;
