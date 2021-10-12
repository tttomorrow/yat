--  @testpoint:opengauss关键字oids(非保留)，作为用户组名


--关键字不带引号-成功
drop group if exists oids;
create group oids with password 'gauss@123';
drop group oids;

--关键字带双引号-成功
drop group if exists "oids";
create group "oids" with password 'gauss@123';
drop group "oids";

--关键字带单引号-合理报错
drop group if exists 'oids';
create group 'oids' with password 'gauss@123';

--关键字带反引号-合理报错
drop group if exists `oids`;
create group `oids` with password 'gauss@123';
