--  @testpoint:opengauss关键字by(非保留)，作为游标名
--前置条件
drop table if exists by_test cascade;
create table by_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor by for select * from by_test order by 1;
close by;
end;

--关键字带双引号-成功
start transaction;
cursor "by" for select * from by_test order by 1;
close "by";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'by' for select * from by_test order by 1;
close 'by';
end;

--关键字带反引号-合理报错
start transaction;
cursor `by` for select * from by_test order by 1;
close `by`;
end;

--清理环境
drop table by_test;