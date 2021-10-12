--  @testpoint:opengauss关键字cache(非保留)，作为游标名
--前置条件
drop table if exists cache_test cascade;
create table cache_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor cache for select * from cache_test order by 1;
close cache;
end;

--关键字带双引号-成功
start transaction;
cursor "cache" for select * from cache_test order by 1;
close "cache";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'cache' for select * from cache_test order by 1;
close 'cache';
end;

--关键字带反引号-合理报错
start transaction;
cursor `cache` for select * from cache_test order by 1;
close `cache`;
end;

--清理环境
drop table cache_test;