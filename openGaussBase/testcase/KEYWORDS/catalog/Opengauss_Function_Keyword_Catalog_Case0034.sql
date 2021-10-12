--  @testpoint:opengauss关键字catalog(非保留)，作为游标名
--前置条件
drop table if exists catalog_test cascade;
create table catalog_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor catalog for select * from catalog_test order by 1;
close catalog;
end;

--关键字带双引号-成功
start transaction;
cursor "catalog" for select * from catalog_test order by 1;
close "catalog";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'catalog' for select * from catalog_test order by 1;
close 'catalog';
end;

--关键字带反引号-合理报错
start transaction;
cursor `catalog` for select * from catalog_test order by 1;
close `catalog`;
end;

--清理环境
drop table catalog_test;