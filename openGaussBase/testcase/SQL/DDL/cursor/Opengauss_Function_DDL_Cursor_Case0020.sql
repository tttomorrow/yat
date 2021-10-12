--  @testpoint:cursor声明游标，使用value子句，子句类型为布尔类型；


start transaction;
cursor cursor20 for values(TRUE,true,1,'1','TRUE','true','t','y','yes'),(FALSE,false,0,'0','FALSE','false','f','n','no');
fetch forward 2 from cursor20;
close cursor20;
end;
