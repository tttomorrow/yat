--  @testpoint:opengauss关键字current_catalog(保留)，作为游标名

--前置条件
drop table if exists current_catalog_test cascade;
create table current_catalog_test(cid int,fid int);

--关键字不带引号-失败
start transaction;
cursor current_catalog for select * from current_catalog_test order by 1;
close current_catalog;
end;

--关键字带双引号-成功
start transaction;
cursor "current_catalog" for select * from current_catalog_test order by 1;
close "current_catalog";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'current_catalog' for select * from current_catalog_test order by 1;
close 'current_catalog';
end;

--关键字带反引号-合理报错
start transaction;
cursor `current_catalog` for select * from current_catalog_test order by 1;
close `current_catalog`;
end;

--清理环境
drop table current_catalog_test cascade;