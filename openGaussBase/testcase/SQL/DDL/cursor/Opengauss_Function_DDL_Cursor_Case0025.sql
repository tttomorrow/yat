--  @testpoint:cursor声明游标，使用value子句，子句类型为网络地址类型；


start transaction;
cursor cursor25 for values(broadcast('192.168.1.5/24'),abbrev(inet '10.1.0.0/16'));
fetch from cursor25;
close cursor25;
end;

