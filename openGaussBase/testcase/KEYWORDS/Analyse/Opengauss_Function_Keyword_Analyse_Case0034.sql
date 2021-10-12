--  @testpoint:opengauss关键字Analyse(保留)，作为游标名

--前置条件
drop table if exists Analyse_test cascade;
create table Analyse_test(cid int,fid int);

--关键字不带引号-失败
start transaction;
cursor Analyse for select * from Analyse_test order by 1;
close Analyse;
end;

--关键字带双引号-成功
start transaction;
cursor "Analyse" for select * from Analyse_test order by 1;
close "Analyse";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'Analyse' for select * from Analyse_test order by 1;
close 'Analyse';
end;

--关键字带反引号-合理报错
start transaction;
cursor `Analyse` for select * from Analyse_test order by 1;
close `Analyse`;
end;

--清理环境
drop table Analyse_test cascade;