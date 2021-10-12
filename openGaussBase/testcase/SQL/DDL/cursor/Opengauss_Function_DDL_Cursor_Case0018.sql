--  @testpoint:cursor声明游标，使用value子句，子句类型为数值类型；


start transaction;
fetch forward 3 from cursor18;
close cursor18;
end;

