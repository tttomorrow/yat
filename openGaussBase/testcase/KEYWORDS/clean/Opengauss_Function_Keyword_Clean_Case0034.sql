--  @testpoint:opengauss关键字clean(非保留)，作为游标名
--前置条件
drop table if exists clean_test cascade;
create table clean_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor clean for select * from clean_test order by 1;
close clean;
end;

--关键字带双引号-成功
start transaction;
cursor "clean" for select * from clean_test order by 1;
close "clean";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'clean' for select * from clean_test order by 1;
close 'clean';
end;

--关键字带反引号-合理报错
start transaction;
cursor `clean` for select * from clean_test order by 1;
close `clean`;
end;

--清理环境
drop table clean_test;