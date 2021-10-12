--  @testpoint:opengauss关键字maxsize非保留)，作为序列名


--关键字不带引号-成功
drop sequence if exists maxsize;
create sequence maxsize start 100 cache 50;
drop sequence maxsize;

--关键字带双引号-成功
drop sequence if exists "maxsize";
create sequence "maxsize" start 100 cache 50;
drop sequence "maxsize";

--关键字带单引号-合理报错
drop sequence if exists 'maxsize';
create sequence 'maxsize' start 100 cache 50;

--关键字带反引号-合理报错
drop sequence if exists `maxsize`;
create sequence `maxsize` start 100 cache 50;
