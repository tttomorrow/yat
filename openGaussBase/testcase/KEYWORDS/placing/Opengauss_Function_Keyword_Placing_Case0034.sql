--  @testpoint:opengauss关键字placing(保留)，作为游标名

--前置条件
drop table if exists placing_test cascade;
create table placing_test(cid int,fid int);

--关键字不带引号-失败
start transaction;
cursor placing for select * from placing_test order by 1;
close placing;
end;

--关键字带双引号-成功
start transaction;
cursor "placing" for select * from placing_test order by 1;
close "placing";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'placing' for select * from placing_test order by 1;
close 'placing';
end;

--关键字带反引号-合理报错
start transaction;
cursor `placing` for select * from placing_test order by 1;
close `placing`;
end;

--清理环境
drop table placing_test cascade;