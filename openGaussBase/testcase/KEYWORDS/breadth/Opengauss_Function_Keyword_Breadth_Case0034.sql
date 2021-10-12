--  @testpoint:opengauss关键字breadth(非保留)，作为游标名
--前置条件
drop table if exists breadth_test cascade;
create table breadth_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor breadth for select * from breadth_test order by 1;
close breadth;
end;

--关键字带双引号-成功
start transaction;
cursor "breadth" for select * from breadth_test order by 1;
close "breadth";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'breadth' for select * from breadth_test order by 1;
close 'breadth';
end;

--关键字带反引号-合理报错
start transaction;
cursor `breadth` for select * from breadth_test order by 1;
close `breadth`;
end;

--清理环境
drop table breadth_test;