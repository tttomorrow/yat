--  @testpoint:cursor声明游标，使用value子句，子句类型为数值类型；


start transaction;
cursor cursor18 for values(0,1),(-32768,32767),(-2147483648,2147483647),(-2147483648,2147483647),(-9223372036854775808,9223372036854775807);
fetch forward 3 from cursor18;
close cursor18;
end;

