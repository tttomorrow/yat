-- @testpoint: opengauss关键字sysdate(保留)，作为游标名,部分测试点合理报错

--前置条件
drop table if exists sysdate_test cascade;
create table sysdate_test(cid int,fid int);

--关键字不带引号-失败
start transaction;
cursor sysdate for select * from sysdate_test order by 1;
close sysdate;
end;

--关键字带双引号-成功
start transaction;
cursor "sysdate" for select * from sysdate_test order by 1;
close "sysdate";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'sysdate' for select * from sysdate_test order by 1;
close 'sysdate';
end;

--关键字带反引号-合理报错
start transaction;
cursor `sysdate` for select * from sysdate_test order by 1;
close `sysdate`;
end;

--清理环境
drop table if exists sysdate_test;