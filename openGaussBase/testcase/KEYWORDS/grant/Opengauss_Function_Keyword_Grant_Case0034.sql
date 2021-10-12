--  @testpoint:opengauss关键字grant(保留)，作为游标名

--前置条件
drop table if exists grant_test cascade;
create table grant_test(cid int,fid int);

--关键字不带引号-失败
start transaction;
cursor grant for select * from grant_test order by 1;
close grant;
end;

--关键字带双引号-成功
start transaction;
cursor "grant" for select * from grant_test order by 1;
close "grant";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'grant' for select * from grant_test order by 1;
close 'grant';
end;

--关键字带反引号-合理报错
start transaction;
cursor `grant` for select * from grant_test order by 1;
close `grant`;
end;

--清理环境
drop table grant_test cascade;