--  @testpoint:cursor声明游标，使用value子句，子句长度为多行；


start transaction;
cursor cursor17 for values(0,1),(1,2),(2,3),(3,4),(4,5) ;
fetch from cursor17;
close cursor17;
end;



