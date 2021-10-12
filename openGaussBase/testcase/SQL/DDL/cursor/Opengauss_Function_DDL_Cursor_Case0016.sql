--  @testpoint:cursor声明游标，使用value子句，子句长度为单行；


start transaction;
cursor cursor16 for values(0,1) ;
fetch from cursor16;
close cursor16;
end;



