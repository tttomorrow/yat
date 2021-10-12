--  @testpoint:opengauss关键字All(保留)，作为游标名

--前置条件
drop table if exists All_test cascade;
create table All_test(cid int,fid int);

--关键字不带引号-失败
start transaction;
cursor All for select * from All_test order by 1;
close All;
end;

--关键字带双引号-成功
start transaction;
cursor "All" for select * from All_test order by 1;
close "All";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'All' for select * from All_test order by 1;
close 'All';
end;

--关键字带反引号-合理报错
start transaction;
cursor `All` for select * from All_test order by 1;
close `All`;
end;

--清理环境
drop table All_test cascade;