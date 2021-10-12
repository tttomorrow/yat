--  @testpoint:opengauss关键字from(保留)，作为游标名

--前置条件
drop table if exists from_test cascade;
create table from_test(cid int,fid int);

--关键字不带引号-失败
start transaction;
cursor from for select * from from_test order by 1;
close from;
end;

--关键字带双引号-成功
start transaction;
cursor "from" for select * from from_test order by 1;
close "from";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'from' for select * from from_test order by 1;
close 'from';
end;

--关键字带反引号-合理报错
start transaction;
cursor `from` for select * from from_test order by 1;
close `from`;
end;

--清理环境
drop table from_test cascade;